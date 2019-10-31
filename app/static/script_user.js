function setUpTooltips() {
  // JavaScript needed for delay

  const tooltipEls = document.querySelectorAll("[data-tooltip]");
  if (!tooltipEls.length) { return }
  tooltipEls.forEach(function (el) {

    function addFocusAndHover(eventTypeIn, eventTypeOut) {
      let timer;
      el.addEventListener(eventTypeIn, function () {
        timer = setTimeout(function () {
          el.dataset.tooltip = "1";
        }, 1000)
      })
      el.addEventListener(eventTypeOut, function () {
        clearTimeout(timer);
        el.dataset.tooltip = "0";
      })
    }

    addFocusAndHover("mouseover", "mouseout");
    addFocusAndHover("focusin", "focusout");
  }
  )
}
setUpTooltips()