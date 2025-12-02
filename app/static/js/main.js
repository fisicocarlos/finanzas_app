let lastScroll = 0;
const nav = document.querySelector("nav");

window.addEventListener("scroll", () => {
  const currentScroll = window.pageYOffset;

  if (currentScroll > lastScroll && currentScroll > 50) {
    nav.classList.add("hidden");
  } else if (currentScroll < lastScroll) {
    nav.classList.remove("hidden");
  }

  lastScroll = currentScroll;
});
