"""技術範疇頁的內容：由團隊成員專長（app/team_profiles.py）濃縮整理而成

成員專長有異動時，請一併檢視這裡的內容是否需要更新。
"""

TECH_STATS = [
    {"value": "10+", "unit": "年", "label": "系統分析與導入經驗"},
    {"value": "8", "unit": "大", "label": "技術範疇一站整合"},
    {"value": "4", "unit": "種", "label": "主流資料庫實務"},
]

TECH_DOMAINS = [
    {
        "title": "需求分析與流程規劃",
        "description": "從營運現場出發，把業務需求整理成可執行的系統規格。",
        "icon": "flow",
        "tags": ["需求訪談", "流程盤點", "As-Is／To-Be 分析", "企業流程再造 BPR", "系統規格文件"],
    },
    {
        "title": "UI/UX 與網站設計",
        "description": "兼顧品牌形象與操作體驗，讓介面清楚、好用、好維護。",
        "icon": "layout",
        "tags": ["網站架構規劃", "UI/UX 設計", "操作流程設計", "響應式網站"],
    },
    {
        "title": "前端開發",
        "description": "以主流框架打造企業後台、資訊看板與各式網站介面。",
        "icon": "code",
        "tags": ["Vue 3", "React", "Next.js", "企業後台", "資訊看板"],
    },
    {
        "title": "後端與 API",
        "description": "模組化架構與前後端分離，承接商業邏輯與即時資料推播。",
        "icon": "server",
        "tags": ["Node.js", "NestJS", "Express", "RESTful API", "WebSocket"],
    },
    {
        "title": "資料庫",
        "description": "從資料模型規劃到查詢分析，確保資料正確、整合順暢。",
        "icon": "database",
        "tags": ["SQL Server", "PostgreSQL", "Oracle", "MySQL", "資料模型設計"],
    },
    {
        "title": "企業系統整合",
        "description": "串接既有系統與第三方服務，打通跨系統的資料流。",
        "icon": "link",
        "tags": ["ERP", "MES", "HR", "POS", "第三方 API 串接", "跨系統資料交換"],
    },
    {
        "title": "AI 應用整合",
        "description": "將 AI 導入實際作業情境，讓知識查找與網站經營更省力。",
        "icon": "spark",
        "tags": ["RAG 智慧問答", "企業知識庫", "AI 功能導入規劃"],
    },
    {
        "title": "專案導入與教育訓練",
        "description": "陪伴系統從測試、訓練到正式上線，降低導入與使用門檻。",
        "icon": "rocket",
        "tags": ["專案管理 PMP", "測試驗證", "教育訓練", "上線導入", "政府標案文件"],
    },
]

TECH_SYSTEMS = [
    "ERP 財務系統",
    "MES 智慧製造系統",
    "POS 營銷系統",
    "HR 人資管理系統",
    "供應商平台",
    "生產即時看板",
    "企業管理平台",
    "政府資訊系統",
    "行動 APP",
]

TECH_FLOW = [
    {"title": "需求理解", "description": "需求訪談、流程盤點，釐清真正要解決的問題。"},
    {"title": "規劃設計", "description": "系統架構、資料模型與介面流程一次規劃到位。"},
    {"title": "開發整合", "description": "前後端開發、資料庫建置與跨系統串接。"},
    {"title": "導入上線", "description": "測試驗證、教育訓練，陪伴系統落實到日常作業。"},
]
