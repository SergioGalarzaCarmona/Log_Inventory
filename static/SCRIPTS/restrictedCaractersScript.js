document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".restricted").forEach(input => {
    input.addEventListener("input", e => {
      e.target.value = e.target.value.replace(/[^a-zA-Z ]/g,'')  
    })
    })
  })
