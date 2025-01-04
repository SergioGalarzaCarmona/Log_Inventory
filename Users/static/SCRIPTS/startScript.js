const container = document.querySelector('.container');
const loginbtn = document.getElementById('login');
const registerbtn = document.getElementById('register');

registerbtn.addEventListener('click', () => {    
    container.classList.add('active');
});

loginbtn.addEventListener('click', () => {
    container.classList.remove('active');
});

