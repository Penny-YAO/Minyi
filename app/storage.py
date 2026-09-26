"""作品圖片 / 影片的儲存位置。

有設定 SUPABASE_URL 與 SUPABASE_SERVICE_KEY 時上傳至 Supabase Storage（正式環境，
重新部署也不會遺失）；否則存在本機 static/uploads/works（開發用）。
"""
import json
import mimetypes
import os
import urllib.error
import urllib.request
import uuid
from urllib.parse import quote

from flask import current_app

LOCAL_URL_PREFIX = "/static/uploads/works/"


class StorageError(Exception):
    pass


def _supabase():
    url = current_app.config.get("SUPABASE_URL", "").rstrip("/")
    key = current_app.config.get("SUPABASE_SERVICE_KEY", "")
    bucket = current_app.config.get("SUPABASE_BUCKET", "works")
    return (url, key, bucket) if url and key else None


def _headers(key, **extra):
    headers = {"apikey": key, **extra}
    # 舊版 service_role 金鑰是 JWT（eyJ 開頭），需同時放在 Authorization；新版 sb_secret_ 金鑰只用 apikey
    if key.startswith("eyJ"):
        headers["Authorization"] = f"Bearer {key}"
    return headers


def _request(method, url, key, data=None, **headers):
    req = urllib.request.Request(url, data=data, method=method, headers=_headers(key, **headers))
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("message", detail)
        except ValueError:
            pass
        raise StorageError(f"Supabase Storage 錯誤（{e.code}）：{detail}") from e
    except urllib.error.URLError as e:
        raise StorageError(f"無法連線至 Supabase Storage：{e.reason}") from e


def save_upload(file_storage, subfolder):
    """儲存上傳檔案，回傳可直接用於 <img>/<video> 的網址；沒有檔案時回傳 None。"""
    if not file_storage or not file_storage.filename:
        return None

    ext = file_storage.filename.rsplit(".", 1)[-1].lower() if "." in file_storage.filename else ""
    unique_name = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex

    supabase = _supabase()
    if not supabase:
        folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
        os.makedirs(folder, exist_ok=True)
        file_storage.save(os.path.join(folder, unique_name))
        return f"{LOCAL_URL_PREFIX}{subfolder}/{unique_name}"

    base_url, key, bucket = supabase
    object_path = f"{subfolder}/{unique_name}"
    content_type = (
        mimetypes.guess_type(unique_name)[0] or file_storage.mimetype or "application/octet-stream"
    )

    stream = file_storage.stream
    stream.seek(0, os.SEEK_END)
    size = stream.tell()
    stream.seek(0)

    _request(
        "POST",
        f"{base_url}/storage/v1/object/{quote(bucket)}/{object_path}",
        key,
        data=stream,
        **{"Content-Type": content_type, "Content-Length": str(size), "x-upsert": "false"},
    )
    return f"{base_url}/storage/v1/object/public/{quote(bucket)}/{object_path}"


def delete_upload(url):
    """刪除先前由本站上傳的檔案；外部連結或刪除失敗都不影響後續流程。"""
    if not url:
        return

    if url.startswith(LOCAL_URL_PREFIX):
        full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], url[len(LOCAL_URL_PREFIX):])
        if os.path.isfile(full_path):
            os.remove(full_path)
        return

    supabase = _supabase()
    if not supabase:
        return
    base_url, key, bucket = supabase
    public_prefix = f"{base_url}/storage/v1/object/public/{quote(bucket)}/"
    if not url.startswith(public_prefix):
        return
    try:
        _request("DELETE", f"{base_url}/storage/v1/object/{quote(bucket)}/{url[len(public_prefix):]}", key)
    except StorageError as e:
        current_app.logger.warning("刪除 Supabase 檔案失敗：%s", e)
