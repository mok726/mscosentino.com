(function () {
  var root = document.documentElement;

  function saved() {
    try { return localStorage.getItem('lang'); } catch (e) { return null; }
  }
  function setLang(l) {
    root.lang = l;
    try { localStorage.setItem('lang', l); } catch (e) {}
    var b = document.getElementById('lang-toggle');
    if (b) b.textContent = l === 'es' ? 'EN' : 'ES';
  }

  var initial = saved() || ((navigator.language || 'es').toLowerCase().indexOf('en') === 0 ? 'en' : 'es');
  setLang(initial);

  document.addEventListener('DOMContentLoaded', function () {
    var b = document.getElementById('lang-toggle');
    if (b) {
      b.textContent = root.lang === 'es' ? 'EN' : 'ES';
      b.addEventListener('click', function () { setLang(root.lang === 'es' ? 'en' : 'es'); });
    }
    var img = document.querySelector('img.avatar');
    if (img) {
      var fallback = function () {
        var d = document.createElement('div');
        d.className = 'avatar';
        d.setAttribute('aria-hidden', 'true');
        d.textContent = 'MC';
        img.replaceWith(d);
      };
      if (img.complete && img.naturalWidth === 0) fallback();
      else img.addEventListener('error', fallback);
    }
    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();
  });
})();

// Email assembled at runtime so it is not sitting in the HTML for scrapers.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-mail-user]').forEach(function (a) {
    var addr = a.dataset.mailUser + '@' + a.dataset.mailDomain;
    a.href = 'mailto:' + addr;
    a.title = addr;
  });
});
