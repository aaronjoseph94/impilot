(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "Close" : "Menu";
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "Menu";
      });
    });
  }

  const counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const end = Number(el.dataset.count || 0);
          const start = performance.now();
          const duration = 1400;
          const tick = (now) => {
            const t = Math.min(1, (now - start) / duration);
            const eased = 1 - (1 - t) * (1 - t);
            el.textContent = String(Math.round(end * eased));
            if (t < 1) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
          io.unobserve(el);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((el) => io.observe(el));
  }

  const bars = document.querySelectorAll(".bar[data-width]");
  if (bars.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const bar = entry.target;
          const fill = bar.querySelector("i");
          if (fill) fill.style.width = `${bar.dataset.width}%`;
          io.unobserve(bar);
        });
      },
      { threshold: 0.4 }
    );
    bars.forEach((el) => io.observe(el));
  }

  const lightbox = document.querySelector(".lightbox");
  const lightboxImg = lightbox?.querySelector("img");
  const lightboxCap = lightbox?.querySelector("p");
  document.querySelectorAll("[data-lightbox]").forEach((fig) => {
    fig.setAttribute("tabindex", "0");
    fig.setAttribute("role", "button");
    fig.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        fig.click();
      }
    });
    fig.addEventListener("click", () => {
      const img = fig.querySelector("img");
      if (!img || !lightbox || !lightboxImg) return;
      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
      if (lightboxCap) lightboxCap.textContent = fig.querySelector("figcaption")?.textContent || "";
      lightbox.classList.add("is-open");
    });
  });
  lightbox?.querySelector(".lightbox-close")?.addEventListener("click", () => {
    lightbox.classList.remove("is-open");
  });
  lightbox?.addEventListener("click", (event) => {
    if (event.target === lightbox) lightbox.classList.remove("is-open");
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") lightbox?.classList.remove("is-open");
  });

  const amounts = document.querySelectorAll("[data-amount]");
  amounts.forEach((btn) => {
    btn.addEventListener("click", () => {
      amounts.forEach((other) => other.classList.remove("is-active"));
      btn.classList.add("is-active");
      const note = document.querySelector("[data-amount-note]");
      if (note) note.textContent = btn.dataset.amount || "";
    });
  });

  const localHost =
    location.protocol === "file:" ||
    location.hostname === "localhost" ||
    location.hostname === "127.0.0.1";

  document.querySelectorAll("form[data-netlify]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) return;
      if (localHost) {
        event.preventDefault();
        window.location.href = "thank-you.html";
      }
    });
  });

  if (header) {
    const onScroll = () => {
      header.style.boxShadow = window.scrollY > 8 ? "0 8px 24px rgba(11,36,40,0.08)" : "none";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
})();
