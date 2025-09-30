
// This script handles both forms for creating a group or a borrowing.(view forms borrowingsGroupForm and borrowingsForm)

const label_borrowing = document.querySelector('.create-borrowing-label');

const closeFormborrowing = document.querySelector(".close-formborrowing");

const create_borrowing = document.getElementById('create-borrowing');
const borrowingsTable = document.querySelector('.borrowings-table__container');


document.addEventListener("DOMContentLoaded", () => {


    function toggleTableVisibility() {
        if (create_borrowing.checked) {
            borrowingsTable.classList.add("hidden");
            closeFormborrowing.classList.remove("hidden");
        } 
        else {
            borrowingsTable.classList.remove("hidden");
            closeFormborrowing.classList.add("hidden");
        }
    }

    create_borrowing.addEventListener("change", toggleTableVisibility);
    
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
    const objectRows = document.querySelectorAll('.object_name');
    const filterText = filterBar.value.toLowerCase();

    objectRows.forEach((object) => {
        const objectParentRow = object.parentElement;
        const objectName = object.textContent.toLowerCase();

        if (!objectName.includes(filterText)) {
            objectParentRow.classList.add('hidden');
        } else {
            objectParentRow.classList.remove('hidden');
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


// edit borrowing
document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.querySelectorAll(".edit-button");
  const modal = document.getElementById("editBorrowingModal");
  const cancelEditBtn = document.getElementById("cancelEdit");
  const confirmEditBtn = document.getElementById("confirmEdit");
  if (editBtn) {
    editBtn.forEach(button => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        modal.style.display = "flex";
      });
    });
  }

  cancelEditBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  confirmEditBtn.addEventListener("click", () => {

  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});