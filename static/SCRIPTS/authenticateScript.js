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


// Handle all close button to alert messages
const closeButtons = document.querySelectorAll('.message-close-button');

closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const alert = button.closest('.message-error, .message-success, .message-warning'); 
    if (alert) {
      alert.classList.add('hidden');
    }
  });
});