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
  const modalTitle = document.querySelector(".modal-title");
  const modalText = document.querySelector(".modal-text");
  const cancelBtn = document.getElementById("cancelCreate");
  const confirmBtn = document.getElementById("confirmCreate");
  if (createBtn) {
    createBtn.addEventListener("click", (e) => {
      const group = document.getElementById("id_group");
      const subuser = document.getElementById("id_in_charge");

      group.addEventListener("change", () => {
        const selectedOption = group.options[group.selectedIndex];
        const inChargeId = selectedOption.dataset.incharge;
        if (inChargeId) {
          subuser.value = inChargeId;
        }
      });
      if (group.value === "") {
        e.preventDefault();
        modalTitle.textContent = "Deseas crear un grupo?";
        modalText.textContent =
          "Para crear un objeto necesitas primero un grupo de objetos.";
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
    create_group.dispatchEvent(new Event("change"));
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
  const modalTitle = document.querySelector(".modal-title");
  const modalText = document.querySelector(".modal-text");
  const cancelBtn = document.getElementById("cancelCreate");
  const confirmBtn = document.getElementById("confirmCreate");
  if (createBtn) {
    const subuser = document.getElementById("in_charge_id");
    createBtn.addEventListener("click", (e) => {
      if (subuser.value === "") {
        e.preventDefault();
        modalTitle.textContent = "Deseas crear un usuario?";
        modalText.textContent =
          "Para crear un grupo de objetos necesitas primero un usuario.";
        modal.style.display = "flex";
      }
    });
  }
  cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmBtn.addEventListener("click", () => {
    const linkButton = document.getElementById("link-button");
    if (modalTitle.textContent === "Deseas crear un usuario?") {
      modal.style.display = "none";
      linkButton.click();
    }
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const deleteBtn = document.getElementById("delete-button");
  const form = document.getElementById('delete-form')
  const modal = document.getElementById("deleteModal");
  const cancelBtn = modal.querySelector("#cancelDelete");
  const confirmBtn = modal.querySelector("#confirmDelete");
  

  function getDeleteCheckboxes() {
    const deleteCheckboxes = document.querySelectorAll('.delete-checkbox');
    const checkedArray = []
    deleteCheckboxes.forEach(checkbox => {
      if (checkbox.checked) {
        checkedArray.push(checkbox)
      }
    })
    return checkedArray
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
    form.submit()
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

// This script handles both forms for creating a group or object.(view Main)

const label_group = document.querySelector(".create-group-label");
const label_object = document.querySelector(".create-object-label");
const deleteLabel = document.querySelector('.delete-object-label')

const closeFormGroup = document.querySelector(".close-formGroup");
const closeFormObject = document.querySelector(".close-formObject");

// FORMS
const formObject = document.querySelector('.create-object')
const formGroup = document.querySelector('.create-group')

const create_group = document.getElementById("create-group");
const create_object = document.getElementById("create-object");
const objects = document.querySelector(".objects-area");

label_group.addEventListener("click", e => {
  if (deleteCheckbox.checked) {
    e.preventDefault()
  }
  else {
    create_object.checked = false;
  }
});
label_object.addEventListener("click", e => {
  if (deleteCheckbox.checked) {
    e.preventDefault()
  }
  else {
    create_group.checked = false;
  }
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


  deleteLabel.addEventListener('click', ()=>{
    create_object.checked = false
    create_group.checked = false
    toggleTableVisibility();
  });
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

document.addEventListener("DOMContentLoaded", () => {
  const objectsContainer = document.querySelector(".objects-area");
  const btnAZ = document.querySelector(".filter-bar__a-z");
  const btnZA = document.querySelector(".filter-bar__z-a");

  function sortObjects(order = "asc") {
    // Get all object cards
    const objects = Array.from(objectsContainer.querySelectorAll(".object-card"));

    // Sort by the <h3 class="object-card__name"> text
    objects.sort((a, b) => {
      const nameA = a
        .querySelector(".object-card__info-container .object-card__name")
        .textContent.toLowerCase()
        .trim();
      const nameB = b
        .querySelector(".object-card__info-container .object-card__name")
        .textContent.toLowerCase()
        .trim();

      return order === "asc"
        ? nameA.localeCompare(nameB)
        : nameB.localeCompare(nameA);
    });

    // Reinsert the cards into the DOM in sorted order
    objects.forEach((object) => objectsContainer.appendChild(object));
  }

  // Bind events
  btnAZ.addEventListener("click", () => sortObjects("asc"));
  btnZA.addEventListener("click", () => sortObjects("desc"));
});