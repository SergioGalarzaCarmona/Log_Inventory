// Handle all close button to alert messages
const closeButtons = document.querySelectorAll(".message-close-button");
console.log(closeButtons);
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

// This script handles the objet image upload functionality for the object image.
const object_image_input = document.getElementById("id_image");
object_image_input.addEventListener("change", function () {
  document.getElementById("id_submit").click();
});

// This script handles the delete button functionality for object images.
const delete_button = document.getElementById("id_delete_button");
delete_button.addEventListener("click", function () {
  const checkbox = document.getElementById("id_delete_checkbox");
  checkbox.checked = true;
  document.getElementById("delete_image").click();
});

// Manage dialog to confirm object deletion
document.addEventListener("DOMContentLoaded", () => {
  const deleteBtn = document.getElementById("delete-button");
  const modal = document.getElementById("deleteModal");
  const cancelBtn = document.getElementById("cancelDelete");
  const confirmBtn = document.getElementById("confirmDelete");
  const deleteForm = document.getElementById("delete-form");

  if (deleteBtn) {
    deleteBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "flex";
    });
  }

  cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmBtn.addEventListener("click", () => {
    deleteForm.submit();
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});
