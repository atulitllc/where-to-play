(function () {
  var key = "wtp-theme";
  function preferred() {
    try {
      var saved = localStorage.getItem(key);
      if (saved === "light" || saved === "dark") return saved;
    } catch (e) {}
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) return "light";
    return "dark";
  }
  function apply(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "light" ? "#e6d8c4" : "#110f0c");
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    var next = theme === "light" ? "dark" : "light";
    btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    btn.textContent = theme === "light" ? "Dark mode" : "Light mode";
    btn.setAttribute("aria-label", "Switch to " + next + " mode");
  }
  apply(preferred());
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("#theme-toggle");
    if (!btn) return;
    var cur = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
    var next = cur === "light" ? "dark" : "light";
    try { localStorage.setItem(key, next); } catch (err) {}
    apply(next);
  });
})();
