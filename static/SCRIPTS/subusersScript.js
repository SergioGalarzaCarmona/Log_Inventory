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

// This script handles both forms for creating a group or a subuser.(view forms subusersGroupForm and subusersForm)
const select = document.getElementById('open-dialog');
select.addEventListener('click', validateGroup)
const label_group = document.querySelector('.create-group-label');
const label_subuser = document.querySelector('.create-subuser-label');
const create_group = document.getElementById('create-group');
const create_subuser = document.getElementById('create-subuser');
label_group.addEventListener('click', function (){
    create_subuser.checked = false; 
});
label_subuser.addEventListener('click', function (){
    create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {
    const subusersTable = document.querySelector('.subusers-table__container');
    const closeFormGroup = document.querySelector(".close-formGroup");
    const closeFormSubuser = document.querySelector(".close-formSubuser");

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