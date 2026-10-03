(function () {
  var q = document.getElementById("q");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chips button"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
  var empty = document.getElementById("empty");
  var count = document.getElementById("count");
  var system = "all";

  function apply() {
    var query = (q.value || "").trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (card) {
      var hay = (card.getAttribute("data-hay") || "").toLowerCase();
      var sys = card.getAttribute("data-system");
      var ok = (system === "all" || sys === system) && (!query || hay.indexOf(query) !== -1);
      card.hidden = !ok;
      if (ok) shown += 1;
    });
    count.textContent = "Showing " + shown + " of " + cards.length;
    empty.classList.toggle("is-on", shown === 0);
  }

  chips.forEach(function (btn) {
    btn.addEventListener("click", function () {
      system = btn.getAttribute("data-system");
      chips.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      apply();
    });
  });
  q.addEventListener("input", apply);
  apply();
})();
