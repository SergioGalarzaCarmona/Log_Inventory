// This script handles that the subuser always belongs to a group, and if the group isn't selected, it opens a dialog to create a new group(subusersGroupForm)
document.addEventListener("DOMContentLoaded", () => {
  const createBtn = document.getElementById("create-button");
  const modal = document.getElementById("createGroupModal");
  const cancelCreateBtn = document.getElementById("cancelCreate");
  const confirmCreateBtn = document.getElementById("confirmCreate");
  if (createBtn) {
    createBtn.addEventListener("click", (e) => {
      const group = document.getElementById("id_group");
      if (group.value === "") {
        e.preventDefault();
        modal.style.display = "flex";
      }
    });
  }

  cancelCreateBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmCreateBtn.addEventListener("click", () => {
    const create_group = document.getElementById("create-group");
    const create_subuser = document.getElementById("create-subuser");
    modal.style.display = "none";
    create_subuser.checked = false;
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
  const deleteButtons = document.querySelectorAll(".delete-button");
  const modal = document.getElementById("deleteModal");
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

// This script handles both forms for creating a group or a subuser.(view forms subusersGroupForm and subusersForm)

const label_group = document.querySelector(".create-group-label");
const label_subuser = document.querySelector(".create-subuser-label");

const closeFormGroup = document.querySelector(".close-formGroup");
const closeFormSubuser = document.querySelector(".close-formSubuser");

const create_group = document.getElementById("create-group");
const create_subuser = document.getElementById("create-subuser");
const groupsContainer = document.querySelector(".groups");

label_group.addEventListener("click", function () {
  create_subuser.checked = false;
});
label_subuser.addEventListener("click", function () {
  create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {
  function toggleTableVisibility() {
    if (create_subuser.checked) {
      groupsContainer.classList.add("hidden");
      closeFormGroup.classList.add("hidden");
      closeFormSubuser.classList.remove("hidden");
    } else if (create_group.checked) {
      groupsContainer.classList.add("hidden");
      closeFormSubuser.classList.add("hidden");
      closeFormGroup.classList.remove("hidden");
    } else {
      groupsContainer.classList.remove("hidden");
      closeFormGroup.classList.add("hidden");
      closeFormSubuser.classList.add("hidden");
    }
  }

  create_subuser.addEventListener("change", toggleTableVisibility);
  create_group.addEventListener("change", toggleTableVisibility);

  toggleTableVisibility();
});

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

// Handle search user in subusers

const filterBar = document.querySelector(".filter-bar__search");

filterBar.addEventListener("input", () => {
  const groups = document.querySelectorAll(".username__container");
  const filterText = filterBar.value.toLowerCase();

  groups.forEach((group) => {
    const groupFather = group.parentElement.parentElement;
    const groupChildren = group.lastElementChild;
    const name = groupChildren.value.toLowerCase();

    if (!name.includes(filterText)) {
      groupFather.classList.add("hidden");
    } else {
      groupFather.classList.remove("hidden");
    }
  });
});

// Handle order buttons

document.addEventListener("DOMContentLoaded", () => {
  const groupsContainer = document.querySelector(".groups");
  const btnAZ = document.querySelector(".filter-bar__a-z");
  const btnZA = document.querySelector(".filter-bar__z-a");

  function sortGroups(order = "asc") {
    // Get all groups
    const groups = Array.from(
      groupsContainer.querySelectorAll(".group-container")
    );

    // Order by the name input value
    groups.sort((a, b) => {
      const nameA = a
        .querySelector(".group-info input[name='name']")
        .value.toLowerCase();
      const nameB = b
        .querySelector(".group-info input[name='name']")
        .value.toLowerCase();

      return order === "asc"
        ? nameA.localeCompare(nameB)
        : nameB.localeCompare(nameA);
    });

    // Reinsert in the DOM in the new order
    groups.forEach((group) => groupsContainer.appendChild(group));
  }

  // Bind buttons
  btnAZ.addEventListener("click", () => sortGroups("asc"));
  btnZA.addEventListener("click", () => sortGroups("desc"));
});
