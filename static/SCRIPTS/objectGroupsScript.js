// Handle all close button to alert messages
const closeButtons = document.querySelectorAll('.message-close-button');

closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const alert = button.closest('.message-error, .message-success, .message-warning'); 
    if (alert) {
      alert.classList.add('hidden');
    }
  });
})
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


// This script handles that the object always belongs to a group, and if the group isn't selected, it opens a dialog to create a new group(object_groupsGroupForm)
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
            document.getElementById('create-object').checked = false;
            object_groups.classList.add("hidden");
            closeFormObject.classList.add("hidden");
            closeFormGroup.classList.remove("hidden");
        });
    }
    else {
        document.getElementById('submit').click();
    }
}
const select = document.getElementById('open-dialog');
select.addEventListener('click', validateGroup)

// This script handles both forms for creating a group or object.(view Main)

const label_group = document.querySelector('.create-group-label');
const label_object = document.querySelector('.create-object-label');

const closeFormGroup = document.querySelector(".close-formGroup"); 
const closeFormObject = document.querySelector(".close-formObject");

const create_group = document.getElementById('create-group');
const create_object = document.getElementById('create-object');
const object_groups = document.querySelector('.groups');

label_group.addEventListener('click', function (){
    create_object.checked = false; 
});
label_object.addEventListener('click', function (){
    create_group.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {


    function toggleTableVisibility() {
        if (create_object.checked) {
            object_groups.classList.add("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormObject.classList.remove("hidden");
        } 
        else if (create_group.checked) {
            object_groups.classList.add("hidden");
            closeFormObject.classList.add("hidden");
            closeFormGroup.classList.remove("hidden");
        }
        else {
            object_groups.classList.remove("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormObject.classList.add("hidden");
        }
    }

    create_object.addEventListener("change", toggleTableVisibility);
    create_group.addEventListener("change", toggleTableVisibility);
    
    toggleTableVisibility();
});

document.querySelectorAll(".group-header").forEach(header => {
  header.addEventListener("click", () => {
    const container = header.parentElement;
    container.classList.toggle("open");
    header.classList.toggle("active");
  });
});
