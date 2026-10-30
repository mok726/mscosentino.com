"""Genera el sitio estático:  python build.py site

Este script NO contiene textos. Todo el contenido vive en la carpeta content/
(ver content/LEEME.txt). Para cambiar o agregar texto se editan esos archivos
y se vuelve a correr este script; el script en sí no hace falta tocarlo.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
OUT = sys.argv[1] if len(sys.argv) > 1 else "site"


# =====================================================================
# Lector de archivos de contenido
# =====================================================================
FIELD = re.compile(r"^([a-z_][a-z0-9_]*)(?:\.(es|en))?:(?:\s+(.*))?$")


class Doc(dict):
    """Diccionario que avisa con claridad cuando falta un campo."""

    def __init__(self, path):
        super().__init__()
        self.path = path

    def __missing__(self, key):
        raise SystemExit(f"Error: falta el campo '{key}' en {self.path}")


def fail(path, n, msg):
    raise SystemExit(f"Error en {path}, línea {n}: {msg}")


def load(path):
    rows = []
    shown = os.path.relpath(path, HERE)
    with open(path, encoding="utf8") as fh:
        for n, raw in enumerate(fh, 1):
            raw = raw.rstrip("\r\n")
            body = raw.strip()
            if not body or body.startswith("#"):
                continue
            lead = raw[: len(raw) - len(raw.lstrip())]
            if "\t" in lead:
                fail(shown, n, "no uses tabuladores para sangrar; usá espacios")
            rows.append((len(lead), body, n))
    pos = 0

    def block(indent):
        return items(indent) if rows[pos][1].startswith("- ") else fields(indent)

    def fields(indent):
        nonlocal pos
        d = Doc(shown)
        while pos < len(rows) and rows[pos][0] >= indent:
            ind, text, n = rows[pos]
            if ind > indent:
                fail(shown, n, "sangría inesperada")
            if text.startswith("- "):
                break
            m = FIELD.match(text)
            if not m:
                fail(shown, n, "se esperaba 'campo: texto' (campo en minúsculas, sin espacios)")
            key, lang, val = m.groups()
            pos += 1
            if val is None:
                if lang:
                    fail(shown, n, f"'{key}.{lang}:' necesita un texto")
                nxt = rows[pos] if pos < len(rows) else None
                if nxt and nxt[0] > indent:
                    d[key] = block(nxt[0])
                elif nxt and nxt[0] == indent and nxt[1].startswith("- "):
                    d[key] = items(indent)
                else:
                    d[key] = []
            elif lang:
                cur = dict.get(d, key)
                if cur is None:
                    cur = d[key] = {}
                elif not isinstance(cur, dict):
                    fail(shown, n, f"'{key}' está definido con y sin .es/.en")
                cur[lang] = val.strip()
            else:
                d[key] = val.strip()
        return d

    def items(indent):
        nonlocal pos
        out = []
        while pos < len(rows) and rows[pos][0] == indent and rows[pos][1].startswith("- "):
            _, text, n = rows[pos]
            body = text[2:].strip()
            if FIELD.match(body):
                rows[pos] = (indent + 2, body, n)
                out.append(fields(indent + 2))
            else:
                out.append(body)
                pos += 1
        return out

    return fields(0) if rows else Doc(shown)


# =====================================================================
# Texto -> HTML
# =====================================================================
def esc(s):
    """Texto plano -> HTML. **negrita** y [texto](https://enlace) están permitidos."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return s


def T(x):
    """Texto simple, o bilingüe ({es, en}), listo para insertar en la página."""
    if isinstance(x, dict):
        es = x.get("es", x.get("en", ""))
        en = x.get("en", es)
        return f'<span lang="es">{esc(es)}</span><span lang="en">{esc(en)}</span>'
    return esc(x)


def ul(items, cls="plain"):
    return f'<ul class="{cls}">' + "".join(f"<li>{T(i)}</li>" for i in items) + "</ul>"


def icon(name):
    return f'<span class="ico i-{name}" aria-hidden="true"></span>'


def gallery(photos):
    if not photos:
        return ""
    figs = "".join(
        f'<figure><img src="/assets/photos/{html.escape(p["file"])}" alt="{html.escape(p["alt"])}" loading="lazy">'
        f'<figcaption>{T(p["caption"])}</figcaption></figure>'
        for p in photos
    )
    return f'<div class="gallery">{figs}</div>'


def btn(href, ico, label, primary=False, **attrs):
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<a class="btn{" primary" if primary else ""}" href="{href}"{extra}>{icon(ico)}{label}</a>'


def card(href, ico, title, text):
    return f'<a class="card" href="{href}">{icon(ico)}<h3>{title}</h3><p>{text}</p></a>'


def joined(*parts):
    return " · ".join(p for p in parts if p)


# =====================================================================
# Contenido
# =====================================================================
site = load(os.path.join(CONTENT, "site.txt"))
ui = load(os.path.join(CONTENT, "ui.txt"))
SITE = site["site_url"].rstrip("/")
NAME = site["name"]

# (ruta, clave del menú, clave en ui.txt)
NAV = [
    ("/", "index.html", "nav_home"),
    ("/cv.html", "cv.html", "nav_cv"),
    ("/projects.html", "projects.html", "nav_projects"),
    ("/courses.html", "courses.html", "nav_courses"),
    ("/certifications.html", "certifications.html", "nav_certs"),
    ("/events.html", "events.html", "nav_events"),
    ("/scout.html", "scout.html", "nav_scout"),
]


def social():
    mail = f'<a class="soc" data-mail-user="{site["email_user"]}" data-mail-domain="{site["email_domain"]}" href="#" aria-label="Email">{icon("mail")}</a>'
    return (
        mail
        + f'<a class="soc" href="{site["linkedin"]}" aria-label="LinkedIn">{icon("linkedin")}</a>'
        + f'<a class="soc" href="{site["github"]}" aria-label="GitHub">{icon("github")}</a>'
        + f'<a class="soc" href="{site["facebook"]}" aria-label="Facebook">{icon("facebook")}</a>'
        + f'<a class="soc" href="{site["x"]}" aria-label="X (personal)">{icon("x")}</a>'
        + f'<a class="soc" href="{site["x_work"]}" aria-label="X ({html.escape(site["x_work_label"])})">{icon("x")}<small>MCT</small></a>'
    )


def page(path, current, title, desc, body):
    nav = "".join(
        f'<a href="{h}"' + (' aria-current="page"' if k == current else "") + f">{T(ui[label])}</a>"
        for h, k, label in NAV
    )
    url = SITE + ("/" if path == "index.html" else "/" + path)
    des = html.escape(desc.get("es", "") if isinstance(desc, dict) else desc)
    den = html.escape(desc.get("en", "") if isinstance(desc, dict) else desc)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {html.escape(NAME)}</title>
<meta name="description" content="{des}">
<meta property="og:title" content="{html.escape(NAME)}">
<meta property="og:description" content="{den}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/assets/photo.jpg">
<meta property="og:url" content="{url}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/site.js"></script>
</head>
<body>
<header class="site"><div class="wrap">
  <a class="brand" href="/">{html.escape(NAME)}</a>
  <nav class="main" aria-label="Principal">{nav}<button id="lang-toggle" class="lang-toggle" type="button" aria-label="Change language / Cambiar idioma">EN</button></nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
  <div class="social">{social()}</div>
  <div>© <span id="year">2026</span> {html.escape(site["full_name"])}</div>
</div></footer>
</body>
</html>
"""


# =====================================================================
# Trabajos: una página por archivo de content/jobs/, en /jobs/<slug>.html
# =====================================================================
def load_jobs():
    jobs = []
    folder = os.path.join(CONTENT, "jobs")
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".txt"):
            continue
        j = load(os.path.join(folder, f))
        # "01-att.txt" -> slug "att" (el número solo define el orden)
        j["slug"] = re.sub(r"^\d+-", "", f[:-4])
        jobs.append(j)
    return jobs


def get(d, key, default=""):
    return dict.get(d, key, default)


def job_meta(j):
    return joined(T(get(j, "role")) if get(j, "role") else "", T(get(j, "period")) if get(j, "period") else "")


def job_page(j):
    parts = [f'<p class="crumb"><a href="/cv.html">← {T(ui["nav_cv"])}</a></p>', f"<h1>{esc(j['company'])}</h1>"]
    meta = job_meta(j)
    if meta:
        parts.append(f'<p class="lead">{meta}</p>')
    parts.append(f"<p>{T(j['summary'])}</p>")
    for r in get(j, "roles", []):
        rmeta = joined(T(r["period"]), esc(get(r, "place")))
        parts.append(
            f"<h2>{T(r['title'])}</h2><p class=\"meta-line\">{rmeta}</p>"
            + (ul(r["bullets"]) if get(r, "bullets") else "")
        )
    if get(j, "resp"):
        parts.append(f'<h2>{T(ui["responsibilities"])}</h2>{ul(j["resp"])}')
    if get(j, "achievements"):
        parts.append(f'<h2>{T(ui["accomplishments"])}</h2>{ul(j["achievements"])}')
    if get(j, "photos"):
        parts.append(f'<h2>{T(ui["photos"])}</h2>{gallery(j["photos"])}')
    return "\n".join(parts)


# =====================================================================
# Creaciones: una página por archivo de content/creations/, en /projects/<slug>.html
# =====================================================================
KIND_ICON = {"software": "code", "3d": "cube", "guide": "book"}


def load_creations():
    out = []
    folder = os.path.join(CONTENT, "creations")
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".txt"):
            continue
        c = load(os.path.join(folder, f))
        c["slug"] = re.sub(r"^\d+-", "", f[:-4])
        if c["kind"] not in KIND_ICON:
            raise SystemExit(
                f"Error: 'kind' en {c.path} debe ser uno de: {', '.join(KIND_ICON)} (dice '{c['kind']}')"
            )
        out.append(c)
    return out


def plain_text(x, lang="es"):
    """Texto sin HTML, para el <title> de la página."""
    return x.get(lang, x.get("es", x.get("en", ""))) if isinstance(x, dict) else x


def link_btn(link, primary=False):
    label = T(link) if get(link, "es") or get(link, "en") else esc(link["site"])
    return btn(link["url"], "link", label, primary=primary)


def item_html(i):
    name, url = i["name"], get(i, "url")
    if not url:
        link = f"<strong>{T(name)}</strong>"
    elif isinstance(name, dict) or isinstance(url, dict):
        link = "".join(
            f'<span lang="{lg}"><a href="{plain_text(url, lg)}">{esc(plain_text(name, lg))}</a></span>' for lg in ("es", "en")
        )
    else:
        link = f'<a href="{url}">{esc(name)}</a>'
    return f"<li>{link}" + (f" — {T(i)}" if get(i, "es") or get(i, "en") else "") + "</li>"


def creation_page(c):
    parts = [f'<p class="crumb"><a href="/projects.html">← {T(ui["nav_projects"])}</a></p>', f"<h1>{T(c['title'])}</h1>"]
    parts.append(f'<p class="lead">{joined(T(ui["kind_" + c["kind"]]), T(c["when"]) if get(c, "when") else "")}</p>')
    parts.append(f"<p>{T(c['summary'])}</p>")
    parts += [f"<p>{T(p)}</p>" for p in get(c, "body", [])]
    if get(c, "items"):
        parts.append(f'<h2>{T(ui["includes"])}</h2><ul class="plain">{"".join(item_html(i) for i in c["items"])}</ul>')
    links = list(get(c, "links", []))
    if c["kind"] == "3d":
        links.append({"site": "Thingiverse", "url": site["thingiverse"] + "/collections",
                      "es": "Mis colecciones en Thingiverse", "en": "My collections on Thingiverse"})
        links.append({"site": "Printables", "url": site["printables"],
                      "es": "Mi perfil en Printables", "en": "My Printables profile"})
    if links:
        parts.append(
            f'<h2>{T(ui["links"])}</h2><p class="links">'
            + "".join(link_btn(l, n == 0) for n, l in enumerate(links))
            + "</p>"
        )
    return "\n".join(parts)


# =====================================================================
# Páginas
# =====================================================================
def home_body(c):
    def tl(i):
        return f'<li><strong>{T(i["year"])}</strong><span class="meta">{T(i)}</span></li>'

    mail = btn("#", "mail", "Email", data_mail_user=site["email_user"], data_mail_domain=site["email_domain"])
    return f"""
<div class="hero">
  <img class="avatar" src="/assets/photo.jpg" alt="{html.escape(NAME)}">
  <div>
    <h1>{html.escape(NAME)}</h1>
    <p class="lead">{T(c["tagline"])}</p>
    <div class="links">
      {btn(site["linkedin"], "linkedin", "LinkedIn", primary=True)}
      {btn(site["github"], "github", "GitHub")}
      {btn(site["facebook"], "facebook", "Facebook")}
      {btn(site["x"], "x", "X")}
      {btn(site["x_work"], "x", esc(site["x_work_label"]))}
      {mail}
    </div>
  </div>
</div>

<h2>{T(c["about_title"])}</h2>
{"".join(f"<p>{T(p)}</p>" for p in c["about"])}
<blockquote>{T(c["quote"])}<cite>{T(c["quote_by"])}</cite></blockquote>

<h2>{T(c["since_title"])}</h2>
<ul class="timeline">
  {"".join(tl(i) for i in c["timeline"])}
</ul>

<div class="cards">
  {card("/cv.html", "work", T(ui["nav_cv"]), T(c["card_cv"]))}
  {card("/projects.html", "code", T(ui["nav_projects"]), T(c["card_projects"]))}
  {card("/courses.html", "school", T(ui["nav_courses"]), T(c["card_courses"]))}
  {card("/certifications.html", "verified", T(ui["nav_certs"]), T(c["card_certs"]))}
  {card("/events.html", "event", T(ui["nav_events"]), T(c["card_events"]))}
  {card("/scout.html", "scout", T(ui["nav_scout"]), T(c["card_scout"]))}
</div>
"""


def cv_body(c, jobs):
    jobs_list = "".join(
        f'<li><a class="joblink" href="/jobs/{j["slug"]}.html"><strong>{esc(j["company"])}</strong>'
        + (f'<span class="meta">{job_meta(j)}</span>' if job_meta(j) else "")
        + f'<span class="more">{T(ui["see_details"])} →</span></a></li>'
        for j in jobs
    )
    return f"""
<h1>{T(ui["nav_cv"])}</h1>
<p class="lead">{T(c["lead"])}</p>

<h2>{T(c["work_title"])}</h2>
<ul class="timeline">{jobs_list}</ul>

<h2>{T(c["education_title"])}</h2>
{ul(c["education"])}

<h2>{T(c["recognitions_title"])}</h2>
{ul(c["recognitions"])}

<h2>{T(c["languages_title"])}</h2>
<p>{T(c["languages"])}</p>
"""


def project_card(c, featured=False):
    return (
        f'<a class="card{" featured" if featured else ""}" href="/projects/{c["slug"]}.html">'
        f'{icon(KIND_ICON[c["kind"]])}<h3>{T(c["title"])}</h3><p>{T(c["summary"])}</p></a>'
    )


def projects_body(c, creations):
    by_slug = {x["slug"]: x for x in creations}
    feat = by_slug.get(c["featured"])
    if not feat:
        raise SystemExit(f"Error: 'featured' en {c.path} dice '{c['featured']}', pero no hay esa creación en content/creations/")
    sections = ""
    for s in c["sections"]:
        mine = [x for x in creations if x["kind"] == s["kind"] and x is not feat]
        if not mine:
            continue
        note = f"<p>{T(s['note'])}</p>" if get(s, "note") else ""
        sections += (
            f'<h2 class="projects-sec">{T(s["title"])}</h2>{note}'
            f'<div class="cards">{"".join(project_card(x) for x in mine)}</div>'
        )
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in c["other"])
    profiles = "".join(f'<li><a href="{p["url"]}">{esc(p["site"])}</a> — {T(p)}</li>' for p in c["profiles"])
    colls = "".join(f'<a class="tag" href="{x["url"]}">{esc(x["name"])} ({esc(x["count"])})</a>' for x in c["collections"])
    repos = "".join(f'<li><a href="{r["url"]}">{esc(r["name"])}</a> — {T(r)}</li>' for r in c["github"])
    return f"""
<h1>{T(c["heading"])}</h1>
<p class="lead">{T(c["lead"])}</p>

<h2>{T(c["featured_label"])}</h2>
<div class="cards">{project_card(feat, True)}</div>
{sections}
<h2>{T(c["other_title"])}</h2>
<p>{tags}</p>

<h2>{T(c["profiles_title"])}</h2>
<ul class="plain">{profiles}</ul>

<h2>{T(c["collections_title"])}</h2>
<p>{T(c["collections_note"])}</p>
<p>{colls}</p>

<h2>{T(c["github_title"])}</h2>
<ul class="plain">{repos}</ul>
<p class="links">{btn(site["github"], "github", T(c["all_github"]))}</p>
"""


def courses_body(c):
    hist = "".join(
        f'<li><strong>{T(h["title"])}</strong><span class="meta">{joined(esc(get(h, "date")), T(h["org"]))}</span></li>'
        for h in c["history"]
    )
    return f"""
<h1>{T(c["heading"])}</h1>
<p class="lead">{T(c["lead"])}</p>
<h2>{T(c["recent_title"])}</h2>
{ul(c["recent"])}
<h2>{T(c["history_title"])}</h2>
<ul class="timeline">{hist}</ul>
"""


def certs_body(c):
    certs = "".join(
        f'<details class="cert"><summary>{esc(x["name"])}</summary><p>'
        + "".join(f'<span class="tag">{esc(i)}</span>' for i in x["items"])
        + "</p></details>"
        for x in c["certs"]
    )
    return f"""
<h1>{T(c["heading"])}</h1>
<p class="lead">{T(c["lead"])}</p>
<p><a href="{c["verify_url"]}">{T(c["verify_text"])} →</a></p>
{certs}
"""


def events_body(c):
    def ev(e):
        return (
            f'<li><strong>{T(e["title"])}</strong><span class="meta">{T(e["meta"])}</span>'
            + (f'<p>{T(e["text"])}</p>' if get(e, "text") else "")
            + (ul(e["bullets"]) if get(e, "bullets") else "")
            + "</li>"
        )

    return f"""
<h1>{T(c["heading"])}</h1>
<p class="lead">{T(c["lead"])}</p>
<ul class="timeline">
  {"".join(ev(e) for e in c["events"])}
</ul>
"""


def scout_body(c):
    path = "".join(
        f'<li><strong>{T(i["title"])}</strong><span class="meta">{T(i["period"])}</span></li>' for i in c["path"]
    )
    return f"""
<h1>{T(ui["nav_scout"])}</h1>
<p class="lead">{T(c["lead"])}</p>
<p>{T(c["intro"])}</p>
<h2>{T(c["path_title"])}</h2>
<ul class="timeline">{path}</ul>
<h2>{T(c["recognitions_title"])}</h2>
{ul(c["recognitions"])}
<h2>{T(c["photos_title"])}</h2>
{gallery(c["photos"])}
"""


# =====================================================================
# Generación
# =====================================================================
PAGES = [
    ("index.html", "home", home_body),
    ("cv.html", "cv", None),
    ("projects.html", "projects", None),
    ("courses.html", "courses", courses_body),
    ("certifications.html", "certifications", certs_body),
    ("events.html", "events", events_body),
    ("scout.html", "scout", scout_body),
]

jobs = load_jobs()
creations = load_creations()
os.makedirs(os.path.join(OUT, "jobs"), exist_ok=True)
os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)
for path, name, body_fn in PAGES:
    c = load(os.path.join(CONTENT, name + ".txt"))
    if name == "cv":
        body = cv_body(c, jobs)
    elif name == "projects":
        body = projects_body(c, creations)
    else:
        body = body_fn(c)
    with open(os.path.join(OUT, path), "w", encoding="utf8") as fh:
        fh.write(page(path, path, c["title"], c["desc"], body))
for j in jobs:
    company = j["company"]
    desc = {"es": f"{company} — experiencia laboral.", "en": f"{company} — work experience."}
    with open(os.path.join(OUT, "jobs", j["slug"] + ".html"), "w", encoding="utf8") as fh:
        fh.write(page(f"jobs/{j['slug']}.html", "cv.html", company, desc, job_page(j)))
for c in creations:
    with open(os.path.join(OUT, "projects", c["slug"] + ".html"), "w", encoding="utf8") as fh:
        fh.write(page(f"projects/{c['slug']}.html", "projects.html", plain_text(c["title"]), c["summary"], creation_page(c)))
print("ok", len(PAGES) + len(jobs) + len(creations), "pages")
