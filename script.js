const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));
const modelCards = Array.from(document.querySelectorAll("[data-category]"));
const resultsCount = document.querySelector("[data-results-count]");

const setFilter = (filter) => {
  let visibleCount = 0;

  modelCards.forEach((card) => {
    const isVisible = filter === "all" || card.dataset.category === filter;
    card.hidden = !isVisible;
    if (isVisible) {
      visibleCount += 1;
    }
  });

  filterButtons.forEach((button) => {
    const isActive = button.dataset.filter === filter;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });

  if (resultsCount) {
    resultsCount.textContent = `Showing ${visibleCount} model ${visibleCount === 1 ? "group" : "groups"}`;
  }
};

filterButtons.forEach((button) => {
  button.addEventListener("click", () => setFilter(button.dataset.filter));
});

setFilter("all");

const navLinks = Array.from(document.querySelectorAll(".site-nav a"));
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (!visible) {
      return;
    }

    navLinks.forEach((link) => {
      link.classList.toggle("is-active", link.getAttribute("href") === `#${visible.target.id}`);
    });
  },
  { rootMargin: "-30% 0px -55% 0px", threshold: [0.2, 0.5, 0.8] }
);

sections.forEach((section) => observer.observe(section));
