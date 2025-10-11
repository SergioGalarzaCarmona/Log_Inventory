document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".restricted").forEach(input => {
    input.addEventListener("input", e => {
      const pattern = "/[a-zA-Z]/" 
      const expression = new RegExp(pattern)
      console.log(e.target.value)
      if (!expression.test(e.target.value)) {
        console.log(e.target.value)
        e.preventDefault()
      }
    })
  })
})