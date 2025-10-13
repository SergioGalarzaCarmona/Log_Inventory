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
// This script handles the subprofiles group image upload and deletion functionality.(subprofiles group)
document.querySelectorAll('input[type="file"]').forEach((input) => {
  input.addEventListener("change", () => {
    id = input.id;
    instance_id = id.split("_")[2];
    const button_submit = document.getElementById(`id_submit_${instance_id}`);
    if (button_submit) {
      button_submit.click();
    }
  });
});

// This script handles that the object always belongs to a group, and if the group isn't selected, it opens a dialog to create a new group(object_groupsGroupForm)
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

// Manage dialog to confirm group deletion
document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll(".delete-button");
  const modal = document.getElementById("groupDeleteModal");
  const cancelBtn = document.getElementById("cancelDelete");
  const confirmBtn = document.getElementById("confirmDelete");

  let currentForm = null;

  deleteButtons.forEach((deleteBtn) => {
    deleteBtn.addEventListener("click", (e) => {
      e.preventDefault();
      const formId = deleteBtn.getAttribute("form");
      currentForm = document.getElementById(formId);
      modal.style.display = "flex";
    });
  });

  cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
    currentForm = null;
  });

  confirmBtn.addEventListener("click", () => {
    if (currentForm) {
      currentForm.submit();
    }
  });

  // Optional: close modal if click outside
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
      currentForm = null;
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
const object_groups = document.querySelector(".groups");

if (label_group){
  label_group.addEventListener("click", e=> {
  if (deleteCheckbox.checked) {
    e.preventDefault()
  } 
  else {
    document.querySelector('main').scrollTop = 0
    create_object.checked = false;
  }
});
}

if (label_object) {
  label_object.addEventListener("click", e => {
  if (deleteCheckbox.checked) {
    e.preventDefault()
  }
  else {
    document.querySelector('main').scrollTop = 0
    create_group.checked = false;
  }
});
}


document.addEventListener("DOMContentLoaded", () => {
  function toggleTableVisibility() {
    if (create_object.checked) {
      object_groups.classList.add("hidden");
      closeFormGroup.classList.add("hidden");
      closeFormObject.classList.remove("hidden");
    
    } else if (create_group.checked) {
      object_groups.classList.add("hidden");
      closeFormObject.classList.add("hidden");
      closeFormGroup.classList.remove("hidden");
     
    } else {
      object_groups.classList.remove("hidden");
      closeFormGroup.classList.add("hidden");
      closeFormObject.classList.add("hidden");
    }
  }

  create_object.addEventListener("change", toggleTableVisibility);
  create_group.addEventListener("change", toggleTableVisibility);

  if (deleteLabel) {
    deleteLabel.addEventListener('click', ()=> {
    create_object.checked = false;
    create_group.checked = false;
    toggleTableVisibility();
  })

  toggleTableVisibility();
  }

});


document.querySelectorAll(".group-header").forEach((header) => {
    header.addEventListener("click", () => { 
      if (!deleteCheckbox.checked) {
        const container = header.parentElement;
        container.classList.toggle("open");
        header.classList.toggle("active");
      }
    });
});

// Manage functionality of filter and search for object groups
const filterInput = document.getElementById("search-input");

filterInput.addEventListener("input", () => {
  const objects = document.querySelectorAll(".group-title");
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

// filter a-z z-a
document.addEventListener("DOMContentLoaded", () => {
  const groupsContainer = document.querySelector(".groups");
  const btnAZ = document.querySelector(".filter-bar__a-z");
  const btnZA = document.querySelector(".filter-bar__z-a");

  function sortGroups(order = "asc") {
    // Get all group containers
    const groups = Array.from(groupsContainer.querySelectorAll(".group-container"));

    // Sort by the group title
    groups.sort((a, b) => {
      const nameA = a.querySelector(".group-title").textContent.toLowerCase().trim();
      const nameB = b.querySelector(".group-title").textContent.toLowerCase().trim();

      return order === "asc"
        ? nameA.localeCompare(nameB)
        : nameB.localeCompare(nameA);
    });

    // Reinsert groups in the sorted order
    groups.forEach(group => groupsContainer.appendChild(group));
  }

  // Bind sorting buttons
  if (btnAZ) btnAZ.addEventListener("click", () => sortGroups("asc"));
  if (btnZA) btnZA.addEventListener("click", () => sortGroups("desc"));
});