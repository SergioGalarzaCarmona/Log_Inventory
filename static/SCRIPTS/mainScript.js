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

// This script handles that the object always belongs to a group, and if the group isn't selected, it opens a dialog to create a new group(objectsGroupForm)
document.addEventListener("DOMContentLoaded", () => {
  const createBtn = document.getElementById("create-button");
  const modal = document.getElementById("createGroupModal");
  const modalTitle = document.querySelector('.modal-title');
  const modalText = document.querySelector('.modal-text');
  const cancelBtn = document.getElementById("cancelCreate");
  const confirmBtn = document.getElementById("confirmCreate");
  if (createBtn) {
    createBtn.addEventListener("click", (e) => {
      const group = document.getElementById('id_group')
      const subuser= document.getElementById('id_in_charge')

      group.addEventListener('change', () => {
        const selectedOption = group.options[group.selectedIndex];
        const inChargeId = selectedOption.dataset.incharge;
        if (inChargeId) {
          subuser.value = inChargeId
        }
      })
      if (group.value === "") {
        e.preventDefault();
        modalTitle.textContent = "Deseas crear un grupo?"
        modalText.textContent = "Para crear un objeto necesitas primero un grupo de objetos."
        modal.style.display = "flex";

      }
    });
  }

  cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmBtn.addEventListener("click", () => {
    const create_group = document.getElementById("create-group");
    const create_object = document.getElementById("create-object");
    modal.style.display = "none";
    create_object.checked = false;
    create_group.checked = true;
    create_group.dispatchEvent(new Event('change'));
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const createBtn = document.getElementById("create-group-button");
  const modal = document.getElementById("createGroupModal");
  const modalTitle = document.querySelector('.modal-title');
  const modalText = document.querySelector('.modal-text');
  const cancelBtn = document.getElementById("cancelCreate");
  const confirmBtn = document.getElementById("confirmCreate");
  if (createBtn) {
    const subuser = document.getElementById('in_charge_id')
    createBtn.addEventListener("click", (e) => {
      if (subuser.value === "") {
        e.preventDefault();
        modalTitle.textContent = "Deseas crear un usuario?"
        modalText.textContent = "Para crear un grupo de objetos necesitas primero un usuario."
        modal.style.display = "flex";
      }
    }
  )};
  cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmBtn.addEventListener("click", () => {
    const linkButton = document.getElementById('link-button')
    if (modalTitle.textContent === "Deseas crear un usuario?") {   
    modal.style.display = "none";
    linkButton.click()
  }});

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

// This script handles both forms for creating a group or object.(view Main)

const label_group = document.querySelector(".create-group-label");
const label_object = document.querySelector(".create-object-label");

const closeFormGroup = document.querySelector(".close-formGroup");
const closeFormObject = document.querySelector(".close-formObject");

const create_group = document.getElementById("create-group");
const create_object = document.getElementById("create-object");
const objects = document.querySelector(".objects-area");

label_group.addEventListener("click", function () {
  create_object.checked = false;
});
label_object.addEventListener("click", function () {
  create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {
  function toggleTableVisibility() {
    if (create_object.checked) {
      objects.classList.add("hidden");
      closeFormGroup.classList.add("hidden");
      closeFormObject.classList.remove("hidden");
    } else if (create_group.checked) {
      objects.classList.add("hidden");
      closeFormObject.classList.add("hidden");
      closeFormGroup.classList.remove("hidden");
    } else {
      objects.classList.remove("hidden");
      closeFormGroup.classList.add("hidden");
      closeFormObject.classList.add("hidden");
    }
  }

  create_object.addEventListener("change", toggleTableVisibility);
  create_group.addEventListener("change", toggleTableVisibility);

  toggleTableVisibility();
});

// Manage filtering by name for objects.
const filterInput = document.getElementById("search-input");

filterInput.addEventListener("input", () => {
  const objects = document.querySelectorAll(".object-card__name");
  const filterText = filterInput.value.toLowerCase();

  objects.forEach((object) => {
    const objectFather = object.parentElement.parentElement;
    const name = object.textContent.toLowerCase();

    if (!name.includes(filterText)) {
      objectFather.classList.add("hidden");
    } else {
      objectFather.classList.remove("hidden");
    }
  });
});
