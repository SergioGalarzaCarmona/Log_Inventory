document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".restricted").forEach(input => {
    input.addEventListener("input", e => {
      const pattern = "/[a-zA-Z]/" 
      const expression = new RegExp(pattern)
      if (!expression.test(e.target.value)) {
        e.preventDefault()
      }
    })
  })
})