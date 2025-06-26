document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', ()=> {
        id = input.id;
        instance_id = id.split('_')[2];
        const button_submit = document.getElementById(`id_submit_${instance_id}`);
        if (button_submit) {
            button_submit.click();
        }
    });
})

const delete_button = document.getElementById('id_delete_button')
delete_button.addEventListener('click',function () {
    const checkbox = document.getElementById('id_delete_checkbox')
    checkbox.checked = true
    document.getElementById('delete_image').click()
})

const dialog = document.getElementById("modify-confirmation");
document.getElementById("open-dialog").addEventListener("click", () => dialog.showModal());
document.getElementById("close-dialog").addEventListener("click", () => dialog.close());