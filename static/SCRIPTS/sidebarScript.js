const checkbox = document.getElementById('open-menu');

function checkWidth() {
    if (window.innerWidth <= 768) { 
        checkbox.checked = true; 
    } 
    else {
        checkbox.checked = false; 
    }
}

checkWidth();
window.addEventListener('resize', checkWidth); 

const span = document.getElementById('username');
const username = span.textContent;
upperCase = 0;
lowerCase = 0
for (let character of username) {
    if (/[A-Z]/.test(character)) {
        upperCase++;
    }
    else if (/[a-z]/.test(character)) {
        lowerCase++;
    }
}
if (lowerCase == username.length) {
    span.style.fontSize = 1.25 +'rem';
}
else if (upperCase == username.length){
    span.style.fontSize = 1 + 'rem';
}
else {
    span.style.fontSize = 1.15 + 'rem';
}