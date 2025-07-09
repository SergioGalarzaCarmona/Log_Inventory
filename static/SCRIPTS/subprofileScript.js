// this script handles password change functionality if the user is an admin or has the permission to change passwords(subprofilesForm)
const new_password = () => {
    const checkbox = document.getElementById('change_password')
    const pivot_password = document.getElementById('pivot_password')
    const form = document.getElementById('set_password_form')
    const change_password = document.getElementById('open-dialog')
    if (checkbox.checked == true){
        form.style.display = 'block';
        pivot_password.style.display = 'none';
        change_password.style.display = 'none';
    }

    else {
        form.style.display = 'none';
        pivot_password.style.display = 'block';
        change_password.style.display = 'block';
    }
        
}