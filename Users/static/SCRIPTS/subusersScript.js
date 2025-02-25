const select = document.getElementById('id_group');
const dialog = document.getElementById("group-dialog");
const checkbox_group = document.getElementById('create-group');
const checkbox_subuser = document.getElementById('create-subuser');
const form = document.getElementById('form-subuser');
document.getElementById('open-dialog').addEventListener("click", function (){
    let value = select.value;
    if (value === '') {
        document.getElementById("open-dialog").addEventListener("click", () => dialog.showModal())
        document.getElementById("close-dialog").addEventListener("click", () => dialog.close())
        document.getElementById('create').addEventListener("click", function (){
            dialog.close()
            checkbox_group.checked = true;
            checkbox_subuser.checked = false;
        });
    }}
    
);
let click = true;
function inputClick() {
    if (click) {
        document.getElementById('open-dialog').click();
        click = false
    }

}