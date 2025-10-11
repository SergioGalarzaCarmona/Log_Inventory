document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".restricted").forEach(input => {
    input.addEventListener("keydown", e => {
      const expression = /[a-zA-Z]/ 
      if (!expression.test(e.target.value)) {
        e.preventDefault()
      }
    })
  })
})