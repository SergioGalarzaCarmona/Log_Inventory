document.addEventListener('DOMContentLoaded', ()=>{
  const selectChat = document.getElementById('chatSelect')
  selectChat.addEventListener('change', ()=>{
    value = selectChat.value
    window.location.href = `${value}`
  })

  // Manage Chat


})

// Handle all close button to alert messages
const closeButtons = document.querySelectorAll(".message-close-button");

closeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const alert = button.closest(
      ".message-error, .message-success, .message-warning"
    );
    if (alert) {
      alert.classList.add("hidden");
    }
  });
});
