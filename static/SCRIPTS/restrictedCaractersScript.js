document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".restricted").forEach((input) => {
    input.addEventListener("input", (e) => {
      e.target.value = e.target.value.replace(/[^a-zA-Z ]/g, "");
    });
  });

  document.querySelectorAll(".restricted-username").forEach((input) => {
    input.addEventListener("input", (e) => {
      // Elimina únicamente los números
      e.target.value = e.target.value.replace(/[0-9]/g, "");
    });
  });
});
