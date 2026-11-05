/* =====================================================

   MOBILE NAVIGATION

===================================================== */

const menuToggle = document.getElementById("menuToggle");

const nav = document.getElementById("nav");

menuToggle.addEventListener("click", () => {

  const isOpen = nav.classList.toggle("open");

  menuToggle.setAttribute(

    "aria-expanded",

    isOpen

  );

  menuToggle.setAttribute(

    "aria-label",

    isOpen ? "Close navigation menu" : "Open navigation menu"

  );

  menuToggle.textContent = isOpen ? "✕" : "☰";

});

document.addEventListener("keydown", event => {
  if (event.key === "Escape" && nav.classList.contains("open")) {
    nav.classList.remove("open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open navigation menu");
    menuToggle.textContent = "☰";
    menuToggle.focus();
  }
});

/* Close mobile menu after clicking a link */

document.querySelectorAll(".nav a").forEach(link => {

  link.addEventListener("click", () => {

    nav.classList.remove("open");

    menuToggle.setAttribute(

      "aria-expanded",

      "false"

    );

    menuToggle.setAttribute("aria-label", "Open navigation menu");

    menuToggle.textContent = "☰";

  });

});

/* =====================================================

   DARK / LIGHT MODE

===================================================== */

const themeToggle =

  document.getElementById("themeToggle");

const savedTheme =

  localStorage.getItem("kwickbox-theme");

if (savedTheme === "light") {

  document.body.classList.add("light");

  themeToggle.textContent = "☾";

}

themeToggle.addEventListener("click", () => {

  document.body.classList.toggle("light");

  const isLight =

    document.body.classList.contains("light");

  themeToggle.textContent =

    isLight ? "☾" : "☀";

  localStorage.setItem(

    "kwickbox-theme",

    isLight ? "light" : "dark"

  );

});

/* =====================================================

   PROJECT FILTERS

===================================================== */

const filters =

  document.querySelectorAll(".filter");

const projectCards =

  document.querySelectorAll(".project-card");

filters.forEach(filter => {

  filter.addEventListener("click", () => {

    filters.forEach(button => {

      button.classList.remove("active");

    });

    filter.classList.add("active");

    const selectedFilter =

      filter.dataset.filter;

    projectCards.forEach(card => {

      const category =

        card.dataset.category;

      if (

        selectedFilter === "all" ||

        category === selectedFilter

      ) {

        card.style.display = "block";

      } else {

        card.style.display = "none";

      }

    });

  });

});

/* =====================================================

   CONTACT FORM

===================================================== */

const contactForm =

  document.getElementById("contactForm");

const formSuccess =

  document.getElementById("formSuccess");

const customQuoteButtons =

  document.querySelectorAll("[data-focus-target='#contactForm']");

customQuoteButtons.forEach(button => {
  button.addEventListener("click", () => {
    const target = document.querySelector(button.dataset.focusTarget);

    if (!target) return;

    target.scrollIntoView({ behavior: "smooth", block: "center" });
    target.classList.remove("is-highlight");
    void target.offsetWidth;
    target.classList.add("is-highlight");

    window.setTimeout(() => {
      target.classList.remove("is-highlight");
    }, 1600);

    const firstField = target.querySelector("input, textarea");
    if (firstField) {
      firstField.focus({ preventScroll: true });
    }
  });
});

contactForm.addEventListener("submit", async event => {
  event.preventDefault();
  formSuccess.textContent = "";

  try {
    const response = await fetch(contactForm.action, {
      method: "POST",
      body: new FormData(contactForm),
      headers: { "X-Requested-With": "XMLHttpRequest" }
    });
    const result = await response.json();

    if (!response.ok) {
      formSuccess.textContent = result.error ||
        "We couldn't send your message. Please try again.";
      return;
    }

    formSuccess.textContent = result.message;
    contactForm.reset();
  } catch {
    formSuccess.textContent =
      "Couldn't reach the server. Please try again later.";
  }
});

/* =====================================================

   SCROLL REVEAL

===================================================== */

const observer =

  new IntersectionObserver(

    entries => {

      entries.forEach(entry => {

        if (entry.isIntersecting) {

          entry.target.classList.add("visible");

          observer.unobserve(entry.target);

        }

      });

    },

    {

      threshold: 0.12

    }

  );

document

  .querySelectorAll(

    ".section-heading, .skill-card, .project-card, .service-card, .process-step, .contact-container"

  )

  .forEach(element => {

    element.classList.add("reveal");

    observer.observe(element);

  });

/* =====================================================

   CURRENT YEAR

===================================================== */

document.getElementById("year").textContent =

  new Date().getFullYear();