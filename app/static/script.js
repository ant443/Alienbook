(function setUpHiddenLogin() {
  const loginUnhideBtn = document.getElementById("display-login")
  if (!loginUnhideBtn) {
    return
  }

  function displayLoginForm(e) {
    this.classList.add("hidden");
    e.target.nextElementSibling.classList.remove("hidden");
  }
  loginUnhideBtn.addEventListener("click", displayLoginForm);
})();

(function setUpParticles() {
  const rootEl = document.getElementById("particles-js");
  if (!rootEl) {
    return;
  }
  const particlesConfig = "../static/particles.json";
  particlesJS.load("particles-js", particlesConfig, function () {
    console.log("particles.json loaded");
  });
})();


(function setUpRequiredInput() {
  const formEl = document.querySelector("#login-form");
  if (!formEl) {
    return;
  }

  function showRequiredIcon(e) {
    const input = e.target;
    const icon = input.nextElementSibling;
    const msg = icon.nextElementSibling;
    icon.classList.add("exclamation");
    msg.classList.add("login-menu__msg-toggle");
    input.classList.add("login-menu__input--border");
  }

  function preventHTML5Bubble(e) {
    e.preventDefault();
  }

  formEl.addEventListener("focusout", showRequiredIcon);
  formEl.addEventListener("invalid", preventHTML5Bubble, true);

})();

