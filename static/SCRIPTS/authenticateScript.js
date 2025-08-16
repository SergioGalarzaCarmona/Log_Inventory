const container = document.querySelector('.container');
const loginbtn = document.getElementById('login');
const registerbtn = document.getElementById('register');
const loginResponsive = document.getElementById('login-responsive');
const registerResponsive = document.getElementById('register-responsive');

registerbtn.addEventListener('click', () => {    
    container.classList.add('active');
});

loginbtn.addEventListener('click', () => {
    container.classList.remove('active');
});

registerResponsive.addEventListener('click', () => {    
    container.classList.add('active');
});

loginResponsive.addEventListener('click', () => {
    container.classList.remove('active');
});


// Select all close buttons
const closeButtons = document.querySelectorAll('.message-close-button');

closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const alert = button.closest('.message'); // find parent .message
    if (alert) {
      alert.classList.add('hidden'); // fade out (CSS handles hiding)
      // Or remove immediately:
      // alert.remove();
    }
  });
});