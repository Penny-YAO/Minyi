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

// 點擊團隊成員卡片時，展開/收合下方的簡介文字
(function () {
    const cards = document.querySelectorAll(".team-card");
    if (cards.length === 0) return;

    cards.forEach((card) => {
        if (!card.querySelector(".team-bio")) return;

        card.addEventListener("click", () => {
            card.classList.toggle("is-active");
        });
    });
})();
