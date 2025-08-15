const label_users_log = document.querySelector("#subusersLog-label")
const label_groups_log = document.querySelector("#subusersgroupsLog-label")
const users_log = document.querySelector(".subusersLog")
const groups_log = document.querySelector(".subusersgroupsLog")

label_users_log.addEventListener("click", ()=> {
    users_log.classList.remove("hidden")
    groups_log.classList.add("hidden")
})

label_groups_log.addEventListener("click", ()=> {
    users_log.classList.add("hidden")
    groups_log.classList.remove("hidden")
})