// Handle all close button to alert messages
const closeButtons = document.querySelectorAll('.message-close-button');
console.log(closeButtons)
closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const alert = button.closest('.message-error, .message-success, .message-warning'); 
    if (alert) {
      alert.classList.add('hidden');
    }
  });
})


// This script handles the subprofile image upload functionality for the profile image.
const object_image_input = document.getElementById('id_image');
object_image_input.addEventListener('change', function () {
    document.getElementById('id_submit').click()
})

// This script handles the delete button functionality for subprofile images.
const delete_button = document.getElementById('id_delete_button')
delete_button.addEventListener('click',function () {
    const checkbox = document.getElementById('id_delete_checkbox')
    checkbox.checked = true
    document.getElementById('delete_image').click()
})
