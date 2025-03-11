function validateGroup(){
    const select = document.getElementById('id_group');
    const option = select.children[0]
    option.value = 0
    value = select.value;
    if ( value == 0) {
        const dialog = document.getElementById("group-dialog");
        dialog.showModal()
        document.getElementById("close-dialog").addEventListener("click", () => dialog.close())
        document.getElementById('create').addEventListener("click", function (){
            dialog.close()
            document.getElementById('create-group').checked = true;
            document.getElementById('create-subuser').checked = false;
        });
    }
    else {
        document.getElementById('submit').click();
    }
}
const select = document.getElementById('open-dialog');
select.addEventListener('click', validateGroup)
const label_group = document.getElementById('create-group-label');
const label_subuser = document.getElementById('create-subuser-label');
label_group.addEventListener('click', function (){
    document.getElementById('create-subuser').checked = false;
});
label_subuser.addEventListener('click', function (){
    document.getElementById('create-group').checked = false;
});