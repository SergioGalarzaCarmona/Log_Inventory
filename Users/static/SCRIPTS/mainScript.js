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