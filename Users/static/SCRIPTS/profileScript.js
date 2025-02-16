document.addEventListener('DOMContentLoaded', function () {
    const input_image = document.getElementById('id_image')

    input_image.addEventListener('input',function (){
        document.getElementById('id_submit').click()
    })
})


