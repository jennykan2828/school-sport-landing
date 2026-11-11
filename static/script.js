document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".day-card");
  const prevBtn = document.querySelector(".nav-arrow.prev");
  const nextBtn = document.querySelector(".nav-arrow.next");
  const nextButtons = document.querySelectorAll(".next-btn");

  let current = 0;

  function showCard(index) {
    cards.forEach((card, i) => {
      card.classList.toggle("active", i === index);
    });
  }

  function nextCard() {
    current = (current + 1) % cards.length;
    showCard(current);
  }

  function prevCard() {
    current = (current - 1 + cards.length) % cards.length;
    showCard(current);
  }

  // Side arrows
  if (nextBtn) nextBtn.addEventListener("click", nextCard);
  if (prevBtn) prevBtn.addEventListener("click", prevCard);

  // Next buttons inside each card
  nextButtons.forEach((btn) => {
    btn.addEventListener("click", nextCard);
  });

  // Keyboard support
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") nextCard();
    if (e.key === "ArrowLeft") prevCard();
  });
});
