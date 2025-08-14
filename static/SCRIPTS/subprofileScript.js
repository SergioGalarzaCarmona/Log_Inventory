// this script handles password change functionality if the user is an admin or has the permission to change passwords(subprofilesForm)
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