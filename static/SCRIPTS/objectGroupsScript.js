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
  const cancelCreateBtn = document.getElementById("cancelCreate");
  const confirmCreateBtn = document.getElementById("confirmCreate");
  if (createBtn) {
    createBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "flex";
    });
  }

  cancelCreateBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmCreateBtn.addEventListener("click", () => {
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

// Manage dialog to confirm object deletion
// Manage dialog to confirm group deletion
document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll(".delete-button"); // all delete buttons
  const modal = document.getElementById("deleteModal");
  const cancelBtn = document.getElementById("cancelDelete");
  const confirmBtn = document.getElementById("confirmDelete");

  let currentForm = null; // will store the right form to submit

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

label_group.addEventListener("click", function () {
  create_object.checked = false;
});
label_object.addEventListener("click", function () {
  create_group.checked = false;
});

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

  toggleTableVisibility();
});

document.querySelectorAll(".group-header").forEach((header) => {
  header.addEventListener("click", () => {
    const container = header.parentElement;
    container.classList.toggle("open");
    header.classList.toggle("active");
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
