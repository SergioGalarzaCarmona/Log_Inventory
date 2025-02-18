document.addEventListener('DOMContentLoaded', function () {
    const input_image = document.getElementById('id_image')

    input_image.addEventListener('input',function (){
        document.getElementById('id_submit').click()
    })
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