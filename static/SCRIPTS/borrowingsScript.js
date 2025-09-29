
// This script handles both forms for creating a group or a borrowing.(view forms borrowingsGroupForm and borrowingsForm)

const label_group = document.querySelector('.create-group-label');
const label_borrowing = document.querySelector('.create-borrowing-label');

const closeFormGroup = document.querySelector(".close-formGroup");
const closeFormborrowing = document.querySelector(".close-formborrowing");

const create_group = document.getElementById('create-group');
const create_borrowing = document.getElementById('create-borrowing');
const borrowingsTable = document.querySelector('.borrowings-table__container');

label_group.addEventListener('click', function (){
    create_borrowing.checked = false; 
});
label_borrowing.addEventListener('click', function (){
    create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {


    function toggleTableVisibility() {
        if (create_borrowing.checked) {
            borrowingsTable.classList.add("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormborrowing.classList.remove("hidden");
        } 
        else {
            borrowingsTable.classList.remove("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormborrowing.classList.add("hidden");
        }
    }

    create_borrowing.addEventListener("change", toggleTableVisibility);
    create_group.addEventListener("change", toggleTableVisibility);
    
    toggleTableVisibility();
});

// Handle all close button to alert messages
const closeButtons = document.querySelectorAll('.message-close-button');

closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const alert = button.closest('.message-error, .message-success, .message-warning'); 
    if (alert) {
      alert.classList.add('hidden');
    }
  });
});

// Handle search user in borrowings

const filterBar = document.querySelector('.filter-bar__search');

filterBar.addEventListener('input', () => {
    const userRows = document.querySelectorAll('.username');
    const filterText = filterBar.value.toLowerCase();

    userRows.forEach((user) => {
        const userParentRow = user.parentElement;
        const username = user.textContent.toLowerCase();

        if (!username.includes(filterText)) {
            userParentRow.classList.add('hidden');
        } else {
            userParentRow.classList.remove('hidden');
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
  rows.forEach(row => tbody.appendChild(row));
}

// Bind buttons
document.querySelector(".filter-bar__a-z").addEventListener("click", ()=> sortTable("asc"));
document.querySelector(".filter-bar__z-a").addEventListener("click", ()=> sortTable("desc"));
