// this script handles password change functionality if the user is an admin or has the permission to change passwords.
const passwordInput = document.getElementById("id_new_password1");
const passwordConfirm = document.querySelector(".container-password");
const passwordConfirmInput = document.getElementById("id_new_password2");

passwordInput.addEventListener("focus", () => {
  if (passwordInput.value === "passwordNow") {
    passwordInput.value = "";
  }
});

passwordInput.addEventListener("blur", () => {
  if (passwordInput.value === "") {
    passwordInput.value = "passwordNow";
    passwordInput.removeAttribute("required");
    passwordConfirmInput.removeAttribute("required");
  }
});

passwordInput.addEventListener("input", () => {
  passwordInput.setAttribute("required", "");
  passwordConfirmInput.setAttribute("required", "");
  if (passwordInput.value.trim() === "") {
    passwordConfirm.classList.remove("show-password");
    passwordConfirm.classList.add("hidden");
  } else {
    passwordConfirm.classList.remove("hidden");
    passwordConfirm.classList.add("show-password");
  }
});

// This script handles the subprofile image upload functionality for the profile image.
const profile_image_input = document.getElementById("id_image");
profile_image_input.addEventListener("change", function () {
  document.getElementById("id_submit").click();
});

// This script handles the delete button functionality for subprofile images.
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
