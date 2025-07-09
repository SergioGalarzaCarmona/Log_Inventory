// This script handles the profile image upload and deletion functionality.(subprofiles group)
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
// This script handles the profile image upload functionality for the profile image.(profile)
const profile_image_input = document.getElementById('id_image');
profile_image_input.addEventListener('change', function () {
    document.getElementById('id_submit').click()
})


// This script handles the delete button functionality for profile images.(profile)
const delete_button = document.getElementById('id_delete_button')
delete_button.addEventListener('click',function () {
    const checkbox = document.getElementById('id_delete_checkbox')
    checkbox.checked = true
    document.getElementById('delete_image').click()
})

// This script handles the confirmation dialog for modifying profile information.(Change profile and subprofile)
const dialog = document.getElementById("modify-confirmation");
document.getElementById("open-dialog").addEventListener("click", () => dialog.showModal());
document.getElementById("close-dialog").addEventListener("click", () => dialog.close());