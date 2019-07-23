document.getElementById("display-login")
  .addEventListener("click", displayLoginForm);

function displayLoginForm(e) {
  this.classList.add("hidden");
  e.target.nextElementSibling.classList.remove("hidden");
}




