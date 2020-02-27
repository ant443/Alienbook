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

  (function initParticles() {
    const particlesConfig = "../static/particles.json";
    particlesJS.load("particles-js", particlesConfig, function () { });
  })();

  function initPauseBtn(Btn) {
    Btn.classList.remove("particlesImg__btn-hide");
  }

  function pauseBtnClickHandler() {
    function toggleAnimationState(toggledState) {
      pJSDom[0].pJS.particles.move.enable = toggledState
      if (toggledState) {pJSDom[0].pJS.fn.particlesRefresh()}
    }

    function toggleBtnAppearance(btn, animationState) {
      btn.childNodes[0].nodeValue = animationState ? "PLAY" : "PAUSE";
      btn.childNodes[1].classList.toggle("particlesImg__pauseIcon");
      btn.childNodes[1].classList.toggle("particlesImg__playIcon");
    }
    const btn = this;
    const animationState = pJSDom[0].pJS.particles.move.enable;
    toggleAnimationState(!animationState);
    toggleBtnAppearance(btn, animationState);
  }

  const pauseBtn = document.getElementById("pause-btn");
  initPauseBtn(pauseBtn);
  pauseBtn.addEventListener("click", pauseBtnClickHandler, false);
})();

(function setUpValidation() {
  const formEl = document.querySelector("#form");
  if (!formEl) {
    return;
  }

  const showAlertBorder = el => el.classList.add("validation__input--border");
  const showAlertMsg = el => el.classList.add("validation__msg-toggle");
  const showAlertIcon = el => el.classList.add("validation__icon");
  const isInputOrSelect = el => el.willValidate && el.type !== "submit";
  const radioMsgDisplayClass = "validation__msg--visible";

  function addAlerts(input) {
    showAlertBorder(input);
    showAlertMsg(input.parentNode.lastElementChild);
    showAlertIcon(input.parentNode.lastElementChild.previousElementSibling);
  }

  function modifyRadioBorder(hideOrShowBorder, fieldset) {
    const elements = fieldset.querySelectorAll("span");
    for (let el of elements) {
      hideOrShowBorder(el);
    }
  }

  function allFocusedBefore(elements) {
    let allFocused = true;
    for (let el of elements) {
      if (!el.dataset.wasfocused) {
        allFocused = false;
      }
    }
    return allFocused;
  }

  function radioFocusIn(e) {
    const hideAlertBorder = el => el.classList.remove("validation__input--border");
    const hideAlertIcon = el => el.classList.remove("validation__icon");
    function messageStateManagement(radioBtn, fieldset) {
      // start showing a message if invalid+all elements focused before.
      if (!radioBtn.checkValidity() && fieldset.dataset.radio === "1") {
        const message = fieldset.lastElementChild
        message.classList.add(radioMsgDisplayClass);
      }
      // mark element when focused
      if (fieldset.dataset.radio === "") {
        const wrapper = radioBtn.parentElement;
        wrapper.dataset.wasfocused = "1";
      }
    }
    const fieldset = e.target.parentElement.parentElement;
    const icon = fieldset.lastElementChild.previousElementSibling;
    modifyRadioBorder(hideAlertBorder, fieldset);
    hideAlertIcon(icon);
    messageStateManagement(e.target, fieldset);
  }

  function radioClick(e) {
    // Description: prevents message staying after clicked until focused out.
    const fieldset = e.target.parentElement.parentElement;
    const message = fieldset.lastElementChild;
    message.classList.remove(radioMsgDisplayClass);
  }

  function selectFocusIn(e) {
    const fieldset = e.target.parentElement;
    if (fieldset.dataset.select === "1") {
      message = fieldset.lastElementChild;
      showAlertMsg(message);
    }
    if (fieldset.dataset.select === "") {
      e.target.dataset.wasfocused = "1";
    }
  }

  function formFocusOutEvents(e) {
    function radioFocusOut(e) {
      const radioBtn = e.target;
      const fieldset = radioBtn.parentElement.parentElement;
      const wrappers = fieldset.querySelectorAll("span");
      const message = fieldset.lastElementChild;
      modifyRadioBorder(showAlertBorder, fieldset);
      if (fieldset.dataset.radio === "" && allFocusedBefore(wrappers)) {
        fieldset.dataset.radio = 1; // add message onfocusin.
      }
      message.classList.remove(radioMsgDisplayClass);
      if (!radioBtn.checkValidity()) {
        const icon = fieldset.lastElementChild.previousElementSibling
        showAlertIcon(icon);
      }
    }

    function selectFocusOut(e) {
      const fieldset = e.target.parentElement;
      const selects = fieldset.querySelectorAll("select");
      const icon = fieldset.lastElementChild.previousElementSibling;
      if (fieldset.dataset.select === "" && allFocusedBefore(selects)) {
        fieldset.dataset.select = 1; // add message onfocusin.
      }
      showAlertBorder(e.target);
      showAlertIcon(icon);
    }

    if (!isInputOrSelect(e.target)) { return }
    if (e.target.type === "radio") {
      radioFocusOut(e);
    } else if (e.target.nodeName === "SELECT") {
      selectFocusOut(e);
    }
    else {
      addAlerts(e.target);
    }
  }

  function submit(e) {
    function distributeElements(elements) {
      for (let el of elements) {
        if (isInputOrSelect(el)) {
          if (el.type === "radio") {
            const icon = el.parentElement.parentElement.lastElementChild.previousElementSibling;
            !el.checkValidity() && showAlertIcon(icon);
          }
          else {
            addAlerts(el);
          }
        }
        if (el.hasAttribute("data-radio")) {
          modifyRadioBorder(showAlertBorder, el);
          el.dataset.radio = 1; // add message onfocusin.
        }
        if (el.hasAttribute("data-select")) {
          el.dataset.select = 1; // add message onfocusin.
        }
      }
    }

    function ajaxValidation() {
      function httpRequestHandler() {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
          if (httpRequest.status === 200) {
            if (this.response) {
              const msgBox = document.getElementById("ajax-validation-msg");
              msgBox.textContent = this.response;
              msgBox.classList.add("server-validation-msg");
            } else {
              window.location.replace("/login")
            }
          } else {
            alert('There was a problem with the request.');
          }
        }
      }

      function sendhttpRequest(e) {
        httpRequest = new XMLHttpRequest();

        if (!httpRequest) {
          alert('Giving up :( Cannot create an XMLHTTP instance');
          return false;
        }
        httpRequest.onreadystatechange = httpRequestHandler;
        httpRequest.open("POST", "/signup/AJAX");
        let formData = new FormData(e.target);
        httpRequest.send(formData);
      }

      let httpRequest;
      sendhttpRequest(e);
    }

    e.preventDefault();
    const invalidInputs = e.target.querySelectorAll("input:invalid, select:invalid, textarea:invalid")
    if (0 < invalidInputs.length) {
      invalidInputs[0].focus();
      distributeElements(e.target);
    }

    else {
      ajaxValidation();
    }
  }

  formEl.addEventListener("focusout", formFocusOutEvents);
  formEl.addEventListener("submit", submit);
  const radioGroup = formEl.querySelector("[data-radio]");
  const selectGroup = formEl.querySelector("[data-select]");
  radioGroup.addEventListener("focusin", radioFocusIn);
  radioGroup.addEventListener("click", radioClick);
  selectGroup.addEventListener("focusin", selectFocusIn);

})();

(function setUpInvalidLoginFocus() {
  const invalidInput = document.querySelector(".validation__error input")
  if (!invalidInput) { return }
  invalidInput.focus();
})();