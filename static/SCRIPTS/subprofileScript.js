// this script handles password change functionality if the user is an admin or has the permission to change passwords.
const passwordInput = document.getElementById('id_new_password1');
const passwordConfirm = document.querySelector('.container-password');
const passwordConfirmInput = document.getElementById('id_new_password2');

passwordInput.addEventListener('focus', ()=> {
    if (passwordInput.value === 'passwordNow'){
        passwordInput.value = '';
    }
    
});

passwordInput.addEventListener('blur',()=> {
    if (passwordInput.value === '') {
        passwordInput.value = 'passwordNow';
        passwordInput.removeAttribute('required');
        passwordConfirmInput.removeAttribute('required');
    }
});

passwordInput.addEventListener('input',()=> {
    passwordInput.setAttribute('required','')
    passwordConfirmInput.setAttribute('required','')
    if (passwordInput.value.trim() === '') {
        passwordConfirm.classList.remove('show-password');
        passwordConfirm.classList.add('hidden');
    }
    else {
        passwordConfirm.classList.remove('hidden');
        passwordConfirm.classList.add('show-password');
    }
   
})

// This script handles the subprofile image upload functionality for the profile image.
const profile_image_input = document.getElementById('id_image');
profile_image_input.addEventListener('change', function () {
    document.getElementById('id_submit').click()
})

// This script handles the delete button functionality for subprofile images.
const delete_button = document.getElementById('id_delete_button')
delete_button.addEventListener('click',function () {
    const checkbox = document.getElementById('id_delete_checkbox')
    checkbox.checked = true
    document.getElementById('delete_image').click()
})