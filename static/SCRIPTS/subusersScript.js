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
// This script handles both forms for creating a group or a subuser.(view forms subusersGroupForm and subusersForm)

const label_group = document.querySelector(".create-group-label");
const label_subuser = document.querySelector(".create-subuser-label");

const closeFormGroup = document.querySelector(".close-formGroup");
const closeFormSubuser = document.querySelector(".close-formSubuser");

const create_group = document.getElementById("create-group");
const create_subuser = document.getElementById("create-subuser");
const subusersTable = document.querySelector(".subusers-table__container");

label_group.addEventListener("click", function () {
  create_subuser.checked = false;
});
label_subuser.addEventListener("click", function () {
  create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {
  function toggleTableVisibility() {
    if (create_subuser.checked) {
      subusersTable.classList.add("hidden");
      closeFormGroup.classList.add("hidden");
      closeFormSubuser.classList.remove("hidden");
    } else if (create_group.checked) {
      subusersTable.classList.add("hidden");
      closeFormSubuser.classList.add("hidden");
      closeFormGroup.classList.remove("hidden");
    } else {
      subusersTable.classList.remove("hidden");
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
  const userRows = document.querySelectorAll(".username");
  const filterText = filterBar.value.toLowerCase();

  userRows.forEach((user) => {
    const userParentRow = user.parentElement;
    const username = user.textContent.toLowerCase();

    if (!username.includes(filterText)) {
      userParentRow.classList.add("hidden");
    } else {
      userParentRow.classList.remove("hidden");
    }
  });
});

// Handle order buttons

function sortTable(order = "asc") {
  const table = document.querySelector(".subusers-table");
  const tbody = table.querySelector("tbody");

  // Get rows as array
  let rows = Array.from(tbody.querySelectorAll("tr"));

  // Sort by first column (Name)
  rows.sort((a, b) => {
    let nameA = a.cells[1].textContent.trim();
    let nameB = b.cells[1].textContent.trim();

    return order === "asc"
      ? nameA.localeCompare(nameB)
      : nameB.localeCompare(nameA);
  });

  // Re-render
  tbody.innerHTML = "";
  rows.forEach((row) => tbody.appendChild(row));
}

// Bind buttons
document
  .querySelector(".filter-bar__a-z")
  .addEventListener("click", () => sortTable("asc"));
document
  .querySelector(".filter-bar__z-a")
  .addEventListener("click", () => sortTable("desc"));
