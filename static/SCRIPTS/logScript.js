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