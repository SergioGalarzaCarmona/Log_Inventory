const deleteCheckbox = document.querySelector('.delete');
const deleteSelector = document.querySelectorAll('.delete-checkbox');
const deleteOptions = document.querySelector('.delete-options');
const cancelDeleteButton = document.querySelector('.cancel-delete');

document.addEventListener("DOMContentLoaded", () => {


    function toggleDeleteOptions() {
        deleteOptions.classList.toggle('hidden', !deleteCheckbox.checked);
        deleteSelector.forEach(element => {
            element.classList.toggle('hidden', !deleteCheckbox.checked);
        });
    }

    deleteCheckbox.addEventListener('change', () => {
      if (!deleteCheckbox.checked) {
          deleteSelector.forEach(element => {
              element.checked = false;
          });
          toggleDeleteOptions();
      }
      else {
          toggleDeleteOptions();
      }
    });
    
    toggleDeleteOptions();
});