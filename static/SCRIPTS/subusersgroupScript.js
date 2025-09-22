// This script handles that the subuser always belongs to a group, and if the group isn't selected, it opens a dialog to create a new group(subusersGroupForm)
function validateGroup(){
    const subusersGroup = document.querySelector('.groups');
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
            groupsContainer.classList.add('hidden');
            closeFormSubuser.classList.add("hidden");
            closeFormGroup.classList.remove("hidden");
        });
    }
    else {
        document.getElementById('submit').click();
    }
}

const select = document.getElementById('open-dialog');
select.addEventListener('click', validateGroup)

// This script handles the subprofiles group image upload and deletion functionality.(subprofiles group)
document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', ()=> {
        id = input.id;
        instance_id = id.split('_')[2];
        const button_submit = document.getElementById(`id_submit_${instance_id}`);
        if (button_submit) {
            button_submit.click();
        }
    });
})

// This script handles both forms for creating a group or a subuser.(view forms subusersGroupForm and subusersForm)


const label_group = document.querySelector('.create-group-label');
const label_subuser = document.querySelector('.create-subuser-label');

const closeFormGroup = document.querySelector(".close-formGroup");
const closeFormSubuser = document.querySelector(".close-formSubuser");

const create_group = document.getElementById('create-group');
const create_subuser = document.getElementById('create-subuser');
const groupsContainer = document.querySelector('.groups');

label_group.addEventListener('click', function (){
    create_subuser.checked = false; 
});
label_subuser.addEventListener('click', function (){
    create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {


    function toggleTableVisibility() {
        if (create_subuser.checked) {
            groupsContainer.classList.add("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormSubuser.classList.remove("hidden");
        } 
        else if (create_group.checked) {
            groupsContainer.classList.add("hidden");
            closeFormSubuser.classList.add("hidden");
            closeFormGroup.classList.remove("hidden");
        }
        else {
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
    const groups = document.querySelectorAll('.username__container');
    const filterText = filterBar.value.toLowerCase();

    groups.forEach((group) => {
        const groupFather = group.parentElement.parentElement
        const groupChildren = group.lastElementChild;
        const name = groupChildren.value.toLowerCase();

        if (!name.includes(filterText)) {
            groupFather.classList.add('hidden');
        } else {
            groupFather.classList.remove('hidden');
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
        const groups = Array.from(groupsContainer.querySelectorAll(".group-container"));

        // Order by the name input value
        groups.sort((a, b) => {
            const nameA = a.querySelector(".group-info input[name='name']").value.toLowerCase();
            const nameB = b.querySelector(".group-info input[name='name']").value.toLowerCase();

            return order === "asc"
            ? nameA.localeCompare(nameB)
            : nameB.localeCompare(nameA)
        });

        // Reinsert in the DOM in the new order
        groups.forEach(group => groupsContainer.appendChild(group));
    }

    // Bind buttons
    btnAZ.addEventListener("click", () => sortGroups("asc"));
    btnZA.addEventListener("click", () => sortGroups("desc"));
});
