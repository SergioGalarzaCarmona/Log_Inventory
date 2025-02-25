const select = document.getElementById('id_group');
const dialog = document.getElementById("group-dialog");
const checkbox_group = document.getElementById('create-group');
const checkbox_subuser = document.getElementById('create-subuser');
const form = document.getElementById('form-subuser');

document.getElementById('open-dialog').addEventListener("click", function (){
    let value = document.getElementById('id_group').value;
    alert(value)
    if (value == '') {
        document.getElementById("open-dialog").addEventListener("click", () => dialog.showModal())
        document.getElementById("close-dialog").addEventListener("click", () => dialog.close())
        document.getElementById('create').addEventListener("click", function (){
            dialog.close()
            checkbox_group.checked = true;
            checkbox_subuser.checked = false;
        });
    }
});
let click = []
function inputClick() {
    if (click.length == 0) {
        document.getElementById('open-dialog').click();
        click.push('click');
    }

}