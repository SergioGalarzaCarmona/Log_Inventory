document.addEventListener("DOMContentLoaded", () => {
    const subuserscheckbox = document.getElementById("subusersLog");
    const subusersgroupscheckbox = document.getElementById("subusersgroupsLog");
    const subuserslog = document.querySelector(".subusersLog");
    const subusersgroupslog = document.querySelector(".subusersgroupsLog");

    function toggleTableVisibility() {
        if (subusersgroupscheckbox.checked) {
            subuserslog.classList.add("hidden");
            subusersgroupslog.classList.remove("hidden");
        } 
        else if (subuserscheckbox.checked) {
            subusersgroupslog.classList.add("hidden");
            subuserslog.classList.remove("hidden");
        }
        else {
            subuserslog.classList.add("hidden");
            subusersgroupslog.classList.add("hidden");
        }
    }

    subuserscheckbox.addEventListener("change", toggleTableVisibility);
    subusersgroupscheckbox.addEventListener("change", toggleTableVisibility);

    toggleTableVisibility();
});