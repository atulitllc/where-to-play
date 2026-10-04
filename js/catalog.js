(function () {
  var q = document.getElementById("q");
  var sel = document.getElementById("system-select");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chips button"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
  var empty = document.getElementById("empty");
  var count = document.getElementById("count");
  var system = "all";
  if (!q || !cards.length) return;

  function systemsOf(card) {
    var all = [card.getAttribute("data-system")];
    var extra = card.getAttribute("data-also") || "";
    if (extra) all = all.concat(extra.split("|").filter(Boolean));
    return all;
  }

  function apply() {
    var query = (q.value || "").trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (card) {
      var hay = (card.getAttribute("data-hay") || "").toLowerCase();
      var ok = (system === "all" || systemsOf(card).indexOf(system) !== -1) && (!query || hay.indexOf(query) !== -1);
      card.hidden = !ok;
      if (ok) shown += 1;
    });
    count.textContent = "Showing " + shown + " of " + cards.length;
    empty.classList.toggle("is-on", shown === 0);
  }

  function setSystem(next) {
    system = next || "all";
    if (sel) sel.value = system;
    chips.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-system") === system ? "true" : "false");
    });
    apply();
  }

  chips.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setSystem(btn.getAttribute("data-system"));
    });
  });
  if (sel) sel.addEventListener("change", function () { setSystem(sel.value); });
  q.addEventListener("input", apply);
  apply();
})();
