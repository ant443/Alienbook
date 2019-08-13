const loginUnhideBtn = document.getElementById("display-login")
if (loginUnhideBtn) {
  loginUnhideBtn.addEventListener("click", displayLoginForm);
}
function displayLoginForm(e) {
  this.classList.add("hidden");
  e.target.nextElementSibling.classList.remove("hidden");
}

// if (particles) {
const particlesConfig = "../static/particles.json";
particlesJS.load("particles-js", particlesConfig, function () {
  console.log("particles.json loaded");
});