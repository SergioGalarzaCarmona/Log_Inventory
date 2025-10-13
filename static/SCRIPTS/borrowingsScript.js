// This script handles both forms for creating a group or a borrowing.(view forms borrowingsGroupForm and borrowingsForm)

// Arrows
const closeFormCreate = document.querySelector(".close-formCreate");
const closeFormEdit = document.querySelector('.close-formEdit')
// Labels
const labelCreate = document.querySelector('.create-borrowing-label')
const labelsEdit = document.querySelectorAll('.edit-button')
// Checkbox
const createBorrowing = document.getElementById("create-borrowing");
const editBorrowing = document.getElementById("edit-borrowing");
// Forms
const createForm = document.getElementById('create-borrowing-form')
const editForm = document.getElementById('edit-borrowing-form')
// Table
const borrowingsTable = document.querySelector(".borrowings-table__container");

labelCreate.addEventListener('click', ()=>{
  document.querySelector('main').scrollTop = 0
  editBorrowing.checked = false
})

labelsEdit.forEach((label)=>{
  label.addEventListener('click', ()=>{
    document.querySelector('main').scrollTop = 0
    createBorrowing.checked = false
  })
})

document.addEventListener("DOMContentLoaded", () => {
  function toggleTableVisibility() {
    if (createBorrowing.checked) {
      borrowingsTable.classList.add("hidden");
      closeFormEdit.classList.add("hidden")
      editForm.classList.add("hidden")
      closeFormCreate.classList.remove("hidden");
      createForm.classList.remove("hidden")
    } else if (editBorrowing.checked) {
      borrowingsTable.classList.add("hidden");
      closeFormCreate.classList.add("hidden");
      createForm.classList.add("hidden")
      closeFormEdit.classList.remove("hidden")
      editForm.classList.remove("hidden")
    } 
    else {
      borrowingsTable.classList.remove("hidden");
      closeFormCreate.classList.add("hidden");
      createForm.classList.add("hidden")
      closeFormEdit.classList.add("hidden")
      editForm.classList.add("hidden")
    }
  } 

  createBorrowing.addEventListener("change", toggleTableVisibility);
  editBorrowing.addEventListener("change", toggleTableVisibility);

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

// Handle search user in borrowings

const filterBar = document.querySelector(".filter-bar__search");

filterBar.addEventListener("input", () => {
  const objectRows = document.querySelectorAll(".object_name");
  const filterText = filterBar.value.toLowerCase();

  objectRows.forEach((object) => {
    const objectParentRow = object.parentElement;
    const objectName = object.textContent.toLowerCase();

    if (!objectName.includes(filterText)) {
      objectParentRow.classList.add("hidden");
    } else {
      objectParentRow.classList.remove("hidden");
    }
  });
});

// Handle order buttons

function sortTable(order = "asc") {
  const table = document.querySelector(".borrowings-table");
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

// Manage editing of borrowings
document.addEventListener("DOMContentLoaded", () => {
  const cancelBtn = document.getElementById("cancelBtn");

  const borrowingId = document.getElementById("borrowingId");
  const objectSelect = document.getElementById("editObject");
  const inChargeSelect = document.getElementById("editInCharge");
  const stockInput = document.getElementById("editStock");
  const dateLimitInput = document.getElementById("editDateLimit");
  const statusCheck = document.getElementById("editStatus");
  
  document.querySelectorAll(".edit-button").forEach((button) => {
    button.addEventListener("click", () => {
      borrowingId.value = button.dataset.id;
      objectSelect.value = button.dataset.object;
      inChargeSelect.value = button.dataset.inCharge;
      stockInput.value = button.dataset.stock;
      dateLimitInput.value = button.dataset.dateLimit;
      statusCheck.checked = button.dataset.status === "True";
    });
  });
});
