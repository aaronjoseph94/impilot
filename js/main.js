(() => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".nav");

  const setNav = (open) => {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Close" : "Menu";
    document.body.classList.toggle("nav-open", open);
  };

  if (toggle && nav) {
    toggle.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setNav(false)));
    document.addEventListener("click", (event) => {
      if (!nav.classList.contains("is-open")) return;
      if (nav.contains(event.target) || toggle.contains(event.target)) return;
      setNav(false);
    });
  }

  const counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const end = Number(el.dataset.count || 0);
        const start = performance.now();
        const tick = (now) => {
          const t = Math.min(1, (now - start) / 1200);
          el.textContent = String(Math.round(end * (1 - (1 - t) * (1 - t))));
          if (t < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        io.unobserve(el);
      });
    }, { threshold: 0.4 });
    counters.forEach((el) => io.observe(el));
  }

  document.querySelectorAll(".bar[data-width]").forEach((bar) => {
    const fill = () => {
      const el = bar.querySelector("i");
      if (el) el.style.width = `${bar.dataset.width}%`;
    };
    if (!("IntersectionObserver" in window)) {
      fill();
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        fill();
        io.unobserve(bar);
      });
    }, { threshold: 0.2 });
    io.observe(bar);
  });

  const lightbox = document.querySelector(".lightbox");
  const lightboxImg = lightbox?.querySelector("img");
  const lightboxCap = lightbox?.querySelector("p");

  const closeLightbox = () => {
    lightbox?.classList.remove("is-open");
    document.body.classList.remove("lb-open");
  };

  document.querySelectorAll("[data-lightbox]").forEach((fig) => {
    fig.setAttribute("tabindex", "0");
    fig.setAttribute("role", "button");
    const open = () => {
      const img = fig.querySelector("img");
      if (!img || !lightbox || !lightboxImg) return;
      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
      if (lightboxCap) lightboxCap.textContent = fig.querySelector("figcaption")?.textContent || "";
      lightbox.classList.add("is-open");
      document.body.classList.add("lb-open");
    };
    fig.addEventListener("click", open);
    fig.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open();
      }
    });
  });

  lightbox?.querySelector(".lightbox-close")?.addEventListener("click", closeLightbox);
  lightbox?.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    closeLightbox();
    setNav(false);
  });

  document.querySelectorAll("[data-amount]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-amount]").forEach((other) => other.classList.remove("is-active"));
      btn.classList.add("is-active");
      const note = document.querySelector("[data-amount-note]");
      if (note) note.textContent = btn.dataset.amount || "";
    });
  });

  const local =
    location.protocol === "file:" ||
    location.hostname === "localhost" ||
    location.hostname === "127.0.0.1";

  document.querySelectorAll("form[data-netlify]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) return;
      if (local) {
        event.preventDefault();
        window.location.href = "thank-you.html";
      }
    });
  });
})();
