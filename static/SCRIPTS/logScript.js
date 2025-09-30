const label_users_log = document.querySelector("#subusersLog-label")
const label_groups_log = document.querySelector("#subusersgroupsLog-label")
const label_objects_log = document.querySelector("#objectsLog-label")
const label_objectgroups_log = document.querySelector("#objectgroupsLog-label")

const users_log = document.querySelector(".subusersLog")
const groups_log = document.querySelector(".subusersgroupsLog")
const objects_log = document.querySelector('.objectsLog')
const object_groups_log = document.querySelector('.objectgroupsLog')

label_users_log.addEventListener("click", ()=> {
    users_log.classList.remove("hidden")
    groups_log.classList.add("hidden")
    objects_log.classList.add("hidden")
    object_groups_log.classList.add("hidden")
})

label_groups_log.addEventListener("click", ()=> {
    users_log.classList.add("hidden")
    groups_log.classList.remove("hidden")
    objects_log.classList.add("hidden")
    object_groups_log.classList.add("hidden")
})

label_objects_log.addEventListener("click", ()=> {
    users_log.classList.add("hidden")
    groups_log.classList.add("hidden")
    objects_log.classList.remove("hidden")
    object_groups_log.classList.add("hidden")
})

label_objectgroups_log.addEventListener("click", ()=> {
    users_log.classList.add("hidden")
    groups_log.classList.add("hidden")
    objects_log.classList.add("hidden")
    object_groups_log.classList.remove("hidden")
})

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

// Manage filter bar by object 
const filterBar = document.getElementById('search-input')

filterBar.addEventListener('input', () => {
    const Rows = document.querySelectorAll('.data_changed');
    const filterText = filterBar.value.toLowerCase();

    Rows.forEach((row) => {
        const ParentRow = row.parentElement;
        const rowName = row.textContent.toLowerCase();

        if (!rowName.includes(filterText)) {
            ParentRow.classList.add('hidden');
        } else {
            ParentRow.classList.remove('hidden');
        }
    });
});