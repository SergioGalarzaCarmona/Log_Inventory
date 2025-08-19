// This script handles that the subuser always belongs to a group, and if the group isn't selected, it opens a dialog to create a new group(subusersGroupForm)
function validateGroup(){
    const select = document.getElementById('id_group');
    const option = select.children[0]
    option.value = 0
    value = select.value;
    if ( value == 0) {
        const dialog = document.getElementById("group-dialog");
        dialog.showModal()
        document.getElementById("close-dialog").addEventListener("click", () => dialog.close())
        document.getElementById('create').addEventListener("click", function (){
            dialog.close()
            document.getElementById('create-group').checked = true;
            document.getElementById('create-subuser').checked = false;
        });
    }
    else {
        document.getElementById('submit').click();
    }
}
const select = document.getElementById('open-dialog');
select.addEventListener('click', validateGroup)
// This script handles both forms for creating a group or a subuser.(view forms subusersGroupForm and subusersForm)

const label_group = document.querySelector('.create-group-label');
const label_subuser = document.querySelector('.create-subuser-label');

const closeFormGroup = document.querySelector(".close-formGroup");
const closeFormSubuser = document.querySelector(".close-formSubuser");

const create_group = document.getElementById('create-group');
const create_subuser = document.getElementById('create-subuser');
const subusersTable = document.querySelector('.subusers-table__container');

label_group.addEventListener('click', function (){
    create_subuser.checked = false; 
});
label_subuser.addEventListener('click', function (){
    create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {


    function toggleTableVisibility() {
        if (create_subuser.checked) {
            subusersTable.classList.add("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormSubuser.classList.remove("hidden");
        } 
        else if (create_group.checked) {
            subusersTable.classList.add("hidden");
            closeFormSubuser.classList.add("hidden");
            closeFormGroup.classList.remove("hidden");
        }
        else {
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
const closeButtons = document.querySelectorAll('.message-close-button');

closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const alert = button.closest('.message-error, .message-success, .message-warning'); 
    if (alert) {
      alert.classList.add('hidden');
    }
  });
});

// Handle search user in subusers

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