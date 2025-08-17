// This script handles the profile image upload functionality for the profile image.
const profile_image_input = document.getElementById('id_image');
profile_image_input.addEventListener('change', function () {
    document.getElementById('id_submit').click()
})


// This script handles the delete button functionality for profile images.
const delete_button = document.getElementById('id_delete_button')
delete_button.addEventListener('click',function () {
    const checkbox = document.getElementById('id_delete_checkbox')
    checkbox.checked = true
    document.getElementById('delete_image').click()
})

// This script handles the confirmation dialog for modifying profile information.
const dialog = document.getElementById("modify-confirmation");
document.getElementById("open-dialog").addEventListener("click", () => dialog.showModal());
document.getElementById("close-dialog").addEventListener("click", () => dialog.close());

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