(function () {
  var q = document.getElementById("q");
  var sel = document.getElementById("system-select");
  var hits = document.getElementById("hits");
  var empty = document.getElementById("empty");
  var count = document.getElementById("count");
  var shelves = document.getElementById("shelves");
  if (!q || !hits) return;
  var cache = null;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function paint(rows) {
    var query = (q.value || "").trim().toLowerCase();
    if (query.length < 2) {
      hits.hidden = true;
      hits.innerHTML = "";
      if (empty) empty.classList.remove("is-on");
      if (count) count.textContent = "";
      if (shelves) shelves.hidden = false;
      return;
    }
    var found = [];
    for (var i = 0; i < rows.length && found.length < 18; i++) {
      var row = rows[i];
      var hay = (row.t + " " + row.y + " " + row.p).toLowerCase();
      if (hay.indexOf(query) !== -1) found.push(row);
    }
    if (shelves) shelves.hidden = true;
    hits.hidden = false;
    hits.innerHTML = found.map(function (row) {
      return '<li><a href="games/' + encodeURIComponent(row.s) + '/">' + esc(row.t) + '</a> <span>' + esc(row.y) + " · " + esc(row.p) + "</span></li>";
    }).join("");
    if (count) count.textContent = found.length ? ("Showing " + found.length + " matches. Open a system page for the full list.") : "";
    if (empty) empty.classList.toggle("is-on", found.length === 0);
  }

  function ready(rows) {
    cache = rows;
    paint(rows);
  }

  q.addEventListener("input", function () {
    if (cache) paint(cache);
    else fetch("search.json").then(function (r) { return r.json(); }).then(ready);
  });
  if (sel) {
    sel.addEventListener("change", function () {
      if (sel.value) window.location.href = sel.value;
    });
  }
})();
