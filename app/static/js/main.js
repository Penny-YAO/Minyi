// 首頁浮動選單：記錄選單高度供背景區塊預留空間，捲動後切換為白底
(function () {
    const header = document.querySelector(".site-header-overlay");
    if (!header) return;

    function syncHeight() {
        document.documentElement.style.setProperty("--header-h", header.offsetHeight + "px");
    }

    function syncScrolled() {
        header.classList.toggle("is-scrolled", window.scrollY > 10);
    }

    syncHeight();
    syncScrolled();
    window.addEventListener("resize", syncHeight);
    window.addEventListener("scroll", syncScrolled, { passive: true });
})();

// 通用輪播元件：任何帶有 data-carousel 屬性的容器都會套用
(function () {
    const INTERVAL = 5000;

    document.querySelectorAll("[data-carousel]").forEach((root) => {
        const slides = root.querySelectorAll(".carousel-slide");
        if (slides.length === 0) return;

        const dots = root.querySelectorAll(".carousel-dot");
        const prevBtn = root.querySelector(".carousel-prev");
        const nextBtn = root.querySelector(".carousel-next");
        let current = 0;
        let timer = null;

        function goTo(index) {
            slides[current].classList.remove("active");
            if (dots[current]) dots[current].classList.remove("active");
            current = (index + slides.length) % slides.length;
            slides[current].classList.add("active");
            if (dots[current]) dots[current].classList.add("active");
        }

        function next() {
            goTo(current + 1);
        }

        function prev() {
            goTo(current - 1);
        }

        function start() {
            stop();
            if (slides.length > 1) {
                timer = setInterval(next, INTERVAL);
            }
        }

        function stop() {
            if (timer) clearInterval(timer);
        }

        dots.forEach((dot, index) => {
            dot.addEventListener("click", () => {
                goTo(index);
                start();
            });
        });

        if (nextBtn) {
            nextBtn.addEventListener("click", () => {
                next();
                start();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener("click", () => {
                prev();
                start();
            });
        }

        root.addEventListener("mouseenter", stop);
        root.addEventListener("mouseleave", start);

        start();
    });
})();

// 翻頁元件：任何帶有 data-pager 屬性的容器都會套用（服務核心、服務項目）
(function () {
    const FLIP_DURATION = 650;

    document.querySelectorAll("[data-pager]").forEach((root) => {
        const pages = root.querySelectorAll(".pager-page");
        if (pages.length === 0) return;

        const book = root.querySelector(".pager-book");
        const dots = root.querySelectorAll(".pager-dot");
        const prevBtn = root.querySelector(".pager-prev");
        const nextBtn = root.querySelector(".pager-next");
        const counter = root.querySelector(".pager-current");
        let current = 0;

        function goTo(index, direction) {
            index = (index + pages.length) % pages.length;
            if (index === current) return;

            const oldPage = pages[current];
            const newPage = pages[index];

            if (direction > 0) {
                // 下一頁：舊頁翻起離開，新頁在下方出現
                oldPage.classList.add("flip-out");
                oldPage.classList.remove("active");
                newPage.classList.add("active");
                setTimeout(() => oldPage.classList.remove("flip-out"), FLIP_DURATION);
            } else {
                // 上一頁：新頁從翻起的位置蓋回來
                newPage.classList.add("flip-in-start");
                void newPage.offsetWidth;
                newPage.classList.remove("flip-in-start");
                newPage.classList.add("active");
                oldPage.classList.remove("active");
            }

            if (dots[current]) dots[current].classList.remove("active");
            if (dots[index]) dots[index].classList.add("active");
            current = index;
            if (counter) counter.textContent = String(current + 1).padStart(2, "0");
        }

        function next() {
            goTo(current + 1, 1);
        }

        function prev() {
            goTo(current - 1, -1);
        }

        if (nextBtn) nextBtn.addEventListener("click", next);
        if (prevBtn) prevBtn.addEventListener("click", prev);

        dots.forEach((dot, index) => {
            dot.addEventListener("click", () => goTo(index, index > current ? 1 : -1));
        });

        root.tabIndex = 0;
        root.addEventListener("keydown", (e) => {
            if (e.key === "ArrowRight") next();
            if (e.key === "ArrowLeft") prev();
        });

        // 手機左右滑動翻頁
        let startX = null;
        book.addEventListener("pointerdown", (e) => {
            startX = e.clientX;
        });
        book.addEventListener("pointerup", (e) => {
            if (startX === null) return;
            const dx = e.clientX - startX;
            startX = null;
            if (Math.abs(dx) < 40) return;
            if (dx < 0) next();
            else prev();
        });
        book.addEventListener("pointercancel", () => {
            startX = null;
        });
    });
})();

// 捲動至區塊時的淡入動態效果
(function () {
    const revealEls = document.querySelectorAll(".reveal, .reveal-down, .reveal-stagger");
    if (revealEls.length === 0) return;

    if (!("IntersectionObserver" in window)) {
        revealEls.forEach((el) => el.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                entry.target.classList.toggle("is-visible", entry.isIntersecting);
            });
        },
        { threshold: 0.15, rootMargin: "0px 0px -60px 0px" }
    );

    revealEls.forEach((el) => observer.observe(el));
})();

// 團隊成員「查看完整經歷」：開啟對應的經歷對話框
(function () {
    document.querySelectorAll(".team-more").forEach((button) => {
        const dialog = document.getElementById(button.dataset.profile);
        if (!dialog) return;

        button.addEventListener("click", () => dialog.showModal());
    });

    document.querySelectorAll(".profile-dialog").forEach((dialog) => {
        dialog.querySelector(".profile-close").addEventListener("click", () => dialog.close());

        // 點擊對話框外的遮罩區域時關閉
        dialog.addEventListener("click", (event) => {
            if (event.target !== dialog) return;
            const rect = dialog.getBoundingClientRect();
            const inside =
                event.clientX >= rect.left && event.clientX <= rect.right &&
                event.clientY >= rect.top && event.clientY <= rect.bottom;
            if (!inside) dialog.close();
        });
    });
})();
