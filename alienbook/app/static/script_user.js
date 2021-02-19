(function setUpPhoto() {
  const form = document.querySelector("#photo");
  if (!form) { return }
  photo=false;
  if (form.dataset["photo"] && form.dataset["photo"]=="1") {photo=true};

  const submit = form.querySelector("#submitbtn");
  const browse = form.querySelector("#photo");

  // Can't style file upload buttons.
  function hideOriginalBtns() {
    form.classList.remove("photo__form-nojs");
    submit.classList.add("hidden");
    browse.classList.add("off-screen", "photo__browse");
  }

  function createNewBtn() {
    const fakeBrowseBtn = document.createElement("div");
    const icon = document.createElement("i");
    const span = document.createElement("span");
    fakeBrowseBtn.classList.add("photo__fake-browse");
    icon.classList.add("photo__camera");
    span.classList.add("photo__text");
    span.textContent = photo ? "Change Photo" : "Add Photo";
    fakeBrowseBtn.appendChild(icon);
    fakeBrowseBtn.appendChild(span);
    form.appendChild(fakeBrowseBtn);
    fakeBrowseBtn.addEventListener("click", function () {
      browse.click();
    })
  }

  hideOriginalBtns()
  createNewBtn()
  browse.addEventListener("change", function (e) {
    form.submit();
  })
})();


(function setUpMainNav() {
  function showTooltip() {
    timer = setTimeout(function (tooltipEl) {
    if (tooltipEl.classList.contains("has-submenu-open")) { return }
    tooltipEl.dataset.tooltip = "1";
    }, 1000, this);
  }
  
  function hideTooltip() {
    clearTimeout(timer);
    this.dataset.tooltip = "0";
  }

  function setUpTooltips() {
    // (JavaScript needed for delay)
    const tooltipEls = document.querySelectorAll("[data-tooltip]");
    if (!tooltipEls.length) { return }
    tooltipEls.forEach(function (el) {
        el.addEventListener("mouseover", showTooltip);
        el.addEventListener("focusin", showTooltip);
        el.addEventListener("mouseout", hideTooltip);
        el.addEventListener("focusout", hideTooltip);
    });
  }

  function openMenu(iconLink) {
    hideTooltip.bind(iconLink.parentNode)();
    iconLink.parentNode.classList.replace("has-submenu", "has-submenu-open");
    iconLink.setAttribute('aria-expanded', "true");
  }

  function closeMenu(iconLink) {
    iconLink.parentNode.classList.replace("has-submenu-open", "has-submenu");
    iconLink.setAttribute('aria-expanded', "false");
  }

  function toggleSubmenuOnclickIcon(submenuContainer) {
    submenuContainer.querySelector('a').addEventListener("click", function (e) {
      e.preventDefault();
      if (this.parentNode.classList.contains("has-submenu")) {
        openMenu(this);
      } else {
        closeMenu(this);
      }
    });
  }

  function closeSubmenuOnclickOutside() {
    document.addEventListener("click", function(e) {
      if (e.target.closest(".has-submenu-open")) { return }
      const openMenu = document.querySelector(".has-submenu-open");
      if (!openMenu) { return }
      const iconLink = openMenu.querySelector("a");
      closeMenu(iconLink);
    })
  }

  function setUpSubMenu() {
    const submenuContainers = document.querySelectorAll('.has-submenu');
    if (!submenuContainers) { return }
    submenuContainers.forEach(function (el) {
      toggleSubmenuOnclickIcon(el);
    });
    closeSubmenuOnclickOutside();
  }

  let timer;
  setUpTooltips()
  setUpSubMenu()
})();

(function setUpCloseFlashMsgBtn() {
  const warnings = document.querySelector(".alert");
  if (!warnings) { return }
  const close_btn = document.createElement("button");
  close_btn.classList.add("alert__close");
  close_btn.textContent = "x";
  close_btn.setAttribute("aria-label", "close notifications");
  warnings.appendChild(close_btn);
  close_btn.addEventListener("click", function() {
    warnings.classList.add("hidden");
  });
})();


(function setUpSliderBtns() {
  settingsForm = document.querySelector(".settings__form");
  if (!settingsForm) { return }
  const checkboxes = settingsForm.querySelectorAll(".settings__checkbox");

  function replaceCheckboxWithSlider(checkbox) {
    checkbox.classList.add("off-screen");
    // Inject slider btn
    const slider = document.createElement("div");
    const off = document.createElement("span");
    const on = document.createElement("span");
    slider.classList.add("slider");
    slider.setAttribute("aria-hidden", "true");
    off.classList.add("slider__text");
    on.classList.add("slider__text");
    off.textContent = "Off";
    on.textContent = "On";
    slider.appendChild(off);
    slider.appendChild(on);
    const state = document.createElement("div");
    state.classList.add("slider__state");
    if (checkbox.checked) {state.classList.add("slider__state--right-aligned")}
    slider.appendChild(state);
    checkbox.parentElement.appendChild(slider);

    // toggle slider on checkbox click
    checkbox.addEventListener("click", function(e) {
      state.classList.toggle("slider__state--right-aligned");
    })

    // toggle checkbox on slider click
    slider.addEventListener("click", function() {
      state.classList.toggle("slider__state--right-aligned");
      checkbox.checked = checkbox.checked ? false : true;
    })
  }

  checkboxes.forEach(replaceCheckboxWithSlider);
})();


(function setUpDeleteAccountConfirmPopup() {
  function createPopup() {
    const popup = document.createElement("div");
    const msg = document.createElement("p");
    const btnContainer = document.createElement("div");
    const btnNo = document.createElement("button");
    const btnYes = document.createElement("button");
    popup.classList.add("confirm-delete");
    msg.classList.add("confirm-delete__msg");
    btnContainer.classList.add("confirm-delete__btns");
    btnNo.classList.add("btn", "btn--red", "btn--no");
    btnYes.classList.add("btn", "btn--green");
    msg.textContent = "Do you really want to delete your account?";
    btnNo.textContent = "No";
    btnYes.textContent = "Yes";
    btnNo.setAttribute("type", "button");
    btnYes.setAttribute("type", "button");
    popup.setAttribute("role", "dialog");
    popup.setAttribute("aria-describedby", "modal");
    msg.setAttribute("id", "modal");
    btnNo.setAttribute("id", "del-acc-no");
    btnYes.setAttribute("id", "del-acc-yes");
    btnContainer.appendChild(btnNo);
    btnContainer.appendChild(btnYes);
    popup.appendChild(msg);
    popup.appendChild(btnContainer);
    const popupContainer = document.getElementById("popup-container");
    popupContainer.appendChild(popup);
    console.log(popupContainer);
  }

  function activatePopup(e) {
    function yesClick() {
      del_acc_form.submit();
    }

    function noClick() {
      btnYes.removeEventListener("click", yesClick);
      btnNo.removeEventListener("click", noClick);
      document.removeEventListener("click", backgroundClick);
      popupContainer.classList.toggle("hidden");
      popupSiblings.forEach(el => {
        if (el.id !== "popup-container") {
          el.removeAttribute("aria-hidden");
        }
      });
      del_acc_btn.focus();
    }

    function backgroundClick(e) {
      if (e.target.closest(".confirm-delete")) { return }
      btnNo.focus();
    }

    function cycleTabLeft(e) {
      if (e.which === 9 && e.shiftKey) {
        e.preventDefault();
        btnYes.focus();
      }
    }

    function cycleTabRight(e) {
      if (e.which === 9 && !e.shiftKey) {
        e.preventDefault();
        btnNo.focus();
      }
    }

    e.preventDefault();
    const del_acc_form = e.target;
    const del_acc_btn = e.target.lastElementChild;
    const popupContainer = document.getElementById("popup-container");
    const btnNo = document.getElementById("del-acc-no");
    const btnYes = document.getElementById("del-acc-yes");
    popupContainer.classList.toggle("hidden");
    btnNo.focus();
    // hide other page content
    const popupSiblings = Array.from(popupContainer.parentNode.children);
    popupSiblings.forEach(el => {
      if (el.id !== "popup-container") {
        el.setAttribute("aria-hidden", "true");
      }
    });

    btnYes.addEventListener("click", yesClick);
    btnNo.addEventListener("click", noClick);
    document.addEventListener("click", backgroundClick);
    btnNo.addEventListener("keydown", cycleTabLeft);
    btnYes.addEventListener("keydown", cycleTabRight);
  }
  
  const delete_acc_form = document.getElementById("delete_acc_form");
  if (!delete_acc_form) { return }
  createPopup();
  delete_acc_form.addEventListener("submit", activatePopup);
})();