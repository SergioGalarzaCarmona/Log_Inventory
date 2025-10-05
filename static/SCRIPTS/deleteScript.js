const deleteLabel = document.querySelector(".delete-object-label");
const deleteCheckbox = document.querySelector(".delete");
const deleteSelector = document.querySelectorAll(".delete-checkbox");
const deleteOptions = document.querySelector(".delete-options");
const cancelDeleteButton = document.querySelector(".cancel-delete");
const userCounter = document.querySelectorAll(".user-counter");

document.addEventListener("DOMContentLoaded", () => {
  function toggleDeleteOptions() {
    deleteOptions.classList.toggle("hidden", !deleteCheckbox.checked);
    deleteSelector.forEach((element) => {
      element.classList.toggle("hidden", !deleteCheckbox.checked);
    });
    userCounter.forEach((element) => {
      element.classList.toggle("hidden", deleteCheckbox.checked);
    });
  }

  deleteCheckbox.addEventListener("change", () => {
    if (!deleteCheckbox.checked) {
      deleteSelector.forEach((element) => {
        element.checked = false;
      });
      toggleDeleteOptions();
    } else {
      document.querySelectorAll(".table-row").forEach((row) => {
        row.removeAttribute("onclick");
      });
      toggleDeleteOptions();
    }
  });

  toggleDeleteOptions();
});

document.addEventListener("DOMContentLoaded", () => {
  const deleteBtn = document.getElementById("delete-button");
  const form = document.getElementById("delete-form");
  const modal = document.getElementById("deleteModal");
  const cancelBtn = modal.querySelector("#cancelDelete");
  const confirmBtn = modal.querySelector("#confirmDelete");

  function getDeleteCheckboxes() {
    const deleteCheckboxes = document.querySelectorAll(".delete-checkbox");
    const checkedArray = [];
    deleteCheckboxes.forEach((checkbox) => {
      if (checkbox.checked) {
        checkedArray.push(checkbox);
      }
    });
    return checkedArray;
  }

  if (deleteBtn) {
    deleteBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (getDeleteCheckboxes().length != 0) {
        modal.style.display = "flex";
      }
    });
  }
  cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmBtn.addEventListener("click", () => {
    form.submit();
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});
