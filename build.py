"""Generates the static site into the output folder: python build.py site

All user-facing text is bilingual: t(es, en) renders both and CSS shows the active one.
Photos for a job go in site/assets/photos/ and are listed in that job's "photos" below.
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "site"
SITE = "https://mscosentino.com"


def t(es, en):
    return f'<span lang="es">{es}</span><span lang="en">{en}</span>'


def tt(x):
    """Accept a plain string or an (es, en) tuple."""
    return t(*x) if isinstance(x, tuple) else x


def ul(items, cls="plain"):
    return f'<ul class="{cls}">' + "".join(f"<li>{tt(i)}</li>" for i in items) + "</ul>"


def icon(name):
    return f'<span class="ico i-{name}" aria-hidden="true"></span>'


def gallery(photos):
    if not photos:
        return ""
    figs = "".join(
        f'<figure><img src="/assets/photos/{f}" alt="{a}" loading="lazy"><figcaption>{tt(c)}</figcaption></figure>'
        for f, a, c in photos
    )
    return f'<div class="gallery">{figs}</div>'


NAV = [
    ("/", "index.html", t("Inicio", "Home")),
    ("/cv.html", "cv.html", t("Experiencia", "Experience")),
    ("/projects.html", "projects.html", t("Proyectos", "Projects")),
    ("/courses.html", "courses.html", t("Cursos", "Courses")),
    ("/certifications.html", "certifications.html", t("Certificaciones", "Certifications")),
    ("/events.html", "events.html", t("Eventos", "Events")),
    ("/scout.html", "scout.html", "Scout"),
]


def page(path, current, title_es, desc_es, desc_en, body):
    nav = "".join(
        f'<a href="{h}"' + (' aria-current="page"' if k == current else "") + f">{label}</a>"
        for h, k, label in NAV
    )
    url = SITE + ("/" if path == "index.html" else "/" + path)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_es} · Mariano S. Cosentino</title>
<meta name="description" content="{desc_es}">
<meta property="og:title" content="Mariano S. Cosentino">
<meta property="og:description" content="{desc_en}">
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
  <a class="brand" href="/">Mariano S. Cosentino</a>
  <nav class="main" aria-label="Principal">{nav}<button id="lang-toggle" class="lang-toggle" type="button" aria-label="Change language / Cambiar idioma">EN</button></nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
  <div class="social">{social()}</div>
  <div>© <span id="year">2026</span> Mariano Sergio Cosentino</div>
</div></footer>
</body>
</html>
"""


def social():
    return (
        f'<a class="soc" data-mail-user="mariano" data-mail-domain="mscosentino.com" href="#" aria-label="Email">{icon("mail")}</a>'
        f'<a class="soc" href="https://www.linkedin.com/in/mscosentino" aria-label="LinkedIn">{icon("linkedin")}</a>'
        f'<a class="soc" href="https://github.com/mok726" aria-label="GitHub">{icon("github")}</a>'
        f'<a class="soc" href="https://www.facebook.com/mscosentino" aria-label="Facebook">{icon("facebook")}</a>'
        f'<a class="soc" href="https://x.com/mok726" aria-label="X (personal)">{icon("x")}</a>'
        f'<a class="soc" href="https://x.com/MCTArgentina" aria-label="X (MCT Argentina)">{icon("x")}<small>MCT</small></a>'
    )


def btn(href, ico, label, primary=False, **attrs):
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<a class="btn{" primary" if primary else ""}" href="{href}"{extra}>{icon(ico)}{label}</a>'


def card(href, ico, title, text):
    return f'<a class="card" href="{href}">{icon(ico)}<h3>{title}</h3><p>{text}</p></a>'


# =====================================================================
# Jobs: one page each at /jobs/<slug>.html
# =====================================================================
JOBS = [
    dict(
        slug="att", company="AT&amp;T",
        role=t("Area Manager, Information MGT", "Area Manager, Information MGT"),
        period=t("Abr 2016 – Actualidad", "Apr 2016 – Present"),
        summary=("Trabajo en AT&amp;T, en la Provincia de Buenos Aires, Argentina, desde abril de 2016.", "I have worked at AT&amp;T, in Buenos Aires Province, Argentina, since April 2016."),
        roles=[
            dict(title="Area Manager, Information MGT", period=("Ago 2021 – Actualidad", "Aug 2021 – Present"), place="Buenos Aires Province, Argentina", bullets=[]),
            dict(title="Principal", period=("Abr 2017 – Abr 2022", "Apr 2017 – Apr 2022"), place="Greater Buenos Aires", bullets=[
                ("Lideré el grupo de trabajo “ADEX” (Active Directory y Exchange) del contrato TSI de AT&amp;T para nuestra empresa hermana VRIO (DirecTV Latam).", "Led the “ADEX” (Active Directory &amp; Exchange) task force of AT&amp;T’s TSI engagement for our sister company VRIO (DirecTV Latam)."),
                ("Selección, gestión, formación y coaching de un nuevo equipo dedicado a sostener la infraestructura.", "Selection, management, training and coaching of a new team focused on supporting the infrastructure."),
                ("Diseñé, planifiqué e implementé la consolidación de un conjunto heterogéneo de servidores de correo en una solución moderna y coherente de Exchange Server, con redundancia local y geográfica completa.", "Designed, planned and implemented the consolidation of an eclectic collection of email servers into a coherent, modern Exchange Server solution with full local and geographical redundancy."),
                ("Lideré los procesos de modernización y consolidación de todos los servicios de Active Directory dentro de nuestro alcance.", "Led the modernization and consolidation of all Active Directory services within our service scope."),
                ("Desarrollé procesos, manuales y documentación para mejorar la transferencia de conocimiento, la repetibilidad y la satisfacción del cliente.", "Developed processes, manuals and documentation to improve knowledge transfer, repeatability and customer satisfaction."),
                ("Desarrollé, y supervisé el desarrollo de, herramientas de monitoreo y automatización para reducir tiempos de resolución, optimizar recursos y bajar la carga de trabajo.", "Developed, and supervised the development of, monitoring and automation tools to improve resolution times, optimize resource utilization and reduce workload."),
                ("Diseñé y planifiqué el reemplazo de la solución Exchange on-premise por Office 365.", "Designed and planned the replacement of the on-premise Exchange solution with Office 365."),
                ("Seguí actuando como Customer Advocate y nexo entre AT&amp;T TSI (Technology Services International) y nuestra empresa hermana AT&amp;T de México, a la que brindamos servicios de IT: analizar necesidades y proponer cambios o servicios adicionales, documentar procedimientos operativos y establecer buenas prácticas, controlar el cumplimiento de políticas y legislación, dar guía técnica, transmitir requerimientos al equipo, responder consultas a tiempo y capacitar a los clientes.", "Continued acting as Customer Advocate and liaison between AT&amp;T TSI (Technology Services International) and our sister company AT&amp;T de México, to which we provide IT services: analyzing needs and suggesting changes or additional services, documenting operational procedures and establishing best practices, monitoring adherence to policies and legislation, providing technical guidance, passing new requirements to developers and the internal team, answering product queries on time and training customers."),
            ]),
            dict(title="Senior Specialist", period=("Abr 2016 – Abr 2017", "Apr 2016 – Apr 2017"), place="Buenos Aires, Buenos Aires Province, Argentina", bullets=[
                ("Customer Advocate y nexo entre AT&amp;T TSI (Technology Services International) y nuestra empresa hermana AT&amp;T de México, a la que brindamos servicios de IT.", "Customer Advocate and liaison between AT&amp;T TSI (Technology Services International) and our sister company AT&amp;T de México, to which we provide IT services."),
                ("Documentar procedimientos operativos y establecer buenas prácticas; controlar el cumplimiento de políticas corporativas y legislación aplicable.", "Document operational procedures and establish best practices; monitor adherence to corporate policies and applicable legislation."),
                ("Dar guía técnica a los clientes, analizar sus necesidades y transmitir nuevos requerimientos a los desarrolladores y al equipo interno.", "Provide technical guidance to customers, analyze their needs and pass new requirements to developers and the internal team."),
                ("Responder a tiempo las consultas sobre productos y capacitar a los clientes para usarlos eficazmente.", "Address product-related queries on time and train customers to use products effectively."),
            ]),
        ],
        resp=[],
        achievements=[
            ("AT&amp;T Believes Impact Award 2025 — Community Leader (abr 2026)", "AT&amp;T Believes Impact Award 2025 — Community Leader (Apr 2026)"),
            ("AT&amp;T Believes Impact Award 2024 — Community Leader, categoría internacional (abr 2025)", "AT&amp;T Believes Impact Award 2024 — Community Leader, International (Apr 2025)"),
            ("AT&amp;T Believes Impact Award 2023 — Community Leader y Voluntario del Año (abr 2024)", "AT&amp;T Believes Impact Award 2023 — Community Leader and Volunteer of the Year (Apr 2024)"),
            ("2022 AT&amp;T Global Volunteer Award — Voluntariado y servicios a la comunidad (may 2023)", "2022 AT&amp;T Global Volunteer Award — Volunteering and Community Services (May 2023)"),
        ],
        photos=[("att-believes.jpg", "Con la gorra de AT&T Believes", ("Con la gorra de AT&amp;T Believes.", "Wearing the AT&amp;T Believes cap."))],
    ),
    dict(
        slug="ub-docencia", company="Universidad de Belgrano",
        role=t("Profesor — Facultad de Tecnología Informática", "Professor — Faculty of Information Technology"),
        period=t("Mar 2016 – Actualidad", "Mar 2016 – Present"),
        summary=("Docencia en la Facultad de Tecnología Informática, en las carreras de Ingeniería Informática y Licenciatura en Sistemas.", "Teaching at the Faculty of Information Technology, in the Computer Engineering and Systems Degree programs."),
        roles=[
            dict(title=("Profesor", "Professor"), period=("Abr 2021 – Actualidad", "Apr 2021 – Present"), place="On-site", bullets=[
                ("Sistemas Distribuidos — Ingeniería Informática y Licenciatura en Sistemas", "Distributed Systems — Computer Engineering and Systems Degree"),
                ("Sistemas Concurrentes — Ingeniería Informática y Licenciatura en Sistemas", "Concurrent Systems — Computer Engineering and Systems Degree"),
                ("Arquitectura de Computadoras — Ingeniería Informática y Licenciatura en Sistemas", "Computer Architecture — Computer Engineering and Systems Degree"),
            ]),
            dict(title=("Profesor Adjunto Asociado", "Adjunct Associate Professor"), period=("Mar 2016 – Abr 2021", "Mar 2016 – Apr 2021"), place="", bullets=[
                ("Sistemas Distribuidos — Ingeniería Informática y Licenciatura en Sistemas", "Distributed Systems — Computer Engineering and Systems Degree"),
                ("Sistemas Concurrentes — Ingeniería Informática y Licenciatura en Sistemas", "Concurrent Systems — Computer Engineering and Systems Degree"),
                ("Práctica Profesional II — Licenciatura en Sistemas", "Professional Practice II — Systems Degree"),
            ]),
        ],
        resp=[], achievements=[], photos=[],
    ),
    dict(
        slug="mct-freelance", company="MCT Freelance",
        role=t("Microsoft Certified Trainer independiente", "Independent Microsoft Certified Trainer"),
        period=t("1999 – 1 ene 2026", "1999 – 1 Jan 2026"),
        summary=("Capacitación independiente como Microsoft Certified Trainer (MCT), desde 1999 hasta el 1 de enero de 2026.", "Independent training work as a Microsoft Certified Trainer (MCT), from 1999 until 1 January 2026."),
        resp=[], achievements=[], photos=[],
    ),
    dict(
        slug="mct-regional-lead", company="Microsoft Learning",
        role=t("MCT Regional Lead (Argentina) — voluntario ad honorem", "MCT Regional Lead (Argentina) — ad honorem volunteer"),
        period=t("Sep 2012 – Nov 2019", "Sep 2012 – Nov 2019"),
        summary=("Un MCT Regional Lead es una persona elegida por Microsoft, entre un grupo de voluntarios, para interactuar con la comunidad de MCT y canalizar recursos y atender sus inquietudes y necesidades.",
                 "An MCT Regional Lead is someone selected by Microsoft, from a pool of volunteers, to interact with the MCT community in order to channel resources and address MCTs’ concerns and needs."),
        resp=[
            ("Nexo entre los MCT de la región y Microsoft Learning u otros grupos de negocio de Microsoft", "Liaison between regional MCTs and Microsoft Learning and/or other Microsoft business groups"),
            ("Punto de contacto, mentoría y soporte para los MCT de la región", "Point of contact, mentoring and support for MCTs in the region"),
            ("Mentoría de nuevos MCT", "Mentoring new MCTs"),
        ], achievements=[], photos=[],
    ),
    dict(
        slug="interlink-vp-sp", company="Interlink Technologies",
        role=t("AVP IT Infrastructure — Special Projects", "AVP IT Infrastructure — Special Projects"),
        period="Nov 2010 – Sep 2014",
        summary=("Interlink Transport Technologies, Inc., subsidiaria de Mediterranean Shipping Company (USA) Inc., Warren, New Jersey.",
                 "Interlink Transport Technologies, Inc., a subsidiary of Mediterranean Shipping Company (USA) Inc., Warren, New Jersey."),
        resp=[
            ("Planificación, implementación y gestión de proyectos especiales", "Planning, implementation and management of special projects"),
            ("Investigación de nuevas tecnologías", "Research on new technologies"),
            ("Diseño e implementación de pruebas de concepto de soluciones estratégicas", "Design and proof-of-concept implementations of strategic solutions"),
            ("Soporte técnico y resolución de problemas de máximo nivel", "Top-level technical support and troubleshooting"),
            ("Soporte y coordinación regional para las sucursales de Latinoamérica", "Regional support and coordination for Latin America branches"),
        ], achievements=[], photos=[],
    ),
    dict(
        slug="interlink-vp-it", company="Interlink Technologies",
        role=t("AVP IT Infrastructure", "AVP IT Infrastructure"),
        period="Oct 2002 – Oct 2010",
        summary=("Interlink Transport Technologies, Inc., subsidiaria de Mediterranean Shipping Company (USA) Inc., Warren, New Jersey.",
                 "Interlink Transport Technologies, Inc., a subsidiary of Mediterranean Shipping Company (USA) Inc., Warren, New Jersey."),
        resp=[
            ("Dirección directa de un equipo de entre 20 y 30 personas, según la etapa", "Direct management of a team of 20 to 30 people, depending on the period"),
            ("Selección, gestión y coaching del personal de IT", "IT personnel selection, management and coaching"),
            ("Influencia sobre más de 500 sistemas en 30 ubicaciones de todo el mundo", "Influence over 500+ systems in 30 locations around the world"),
            ("Responsable de brindar servicio a más de 1900 usuarios en 3 continentes, las 24 horas, todos los días", "Responsible for providing services to 1900+ users on 3 continents on a 24x7 basis"),
            ("Asistencia internacional en sitio", "International on-site assistance"),
            ("Administración de Exchange (incluyendo los servidores Centera y Legato de EMC)", "Exchange administration (including the EMC Centera and Legato servers)"),
            ("Administración de EMC SAN (incluyendo replicación al sitio de respaldo remoto)", "EMC SAN administration (including replication to the remote backup site)"),
            ("Diseño e implementación de políticas de DR; administración de ISA, planificación y gestión de redes", "Design and implementation of DR policies; ISA administration, network planning and management"),
        ],
        achievements=[
            ("Creé desde cero un datacenter que hoy incluye más de 300 servidores y equipos relacionados, con servicio en 3 continentes, 24x7.", "Created from scratch a datacenter that now includes 300+ servers and related equipment, serving 3 continents, 24x7."),
            ("Seleccioné, formé y dirigí un equipo capaz de sostener esa infraestructura.", "Selected, trained and managed a team capable of supporting this infrastructure."),
            ("Desarrollé manuales de procedimientos, bitácoras de servicio y procedimientos de documentación y monitoreo para asegurar la transferencia de conocimiento y mejorar tiempos de respuesta y calidad.", "Developed procedure manuals, service logs and documentation and monitoring procedures to ensure knowledge transfer and improve response time and quality."),
            ("Diseñé y asistí la reconversión tecnológica de MSC Sudáfrica, capacité a su equipo local y sigo dando soporte.", "Designed and assisted the technological reconversion of MSC South Africa, trained their local team and still provide support."),
            ("Planifiqué y dirigí la actualización de hardware y software de MSC USA con un equipo de 12 personas: migración de infraestructura Windows de NT 4 / 2000 a 2003, Exchange 5.5 a 2003 SP1, más de 800 estaciones de trabajo y 40 servidores en sucursales, y administración remota centralizada que eliminó la necesidad de equipos de IT locales.", "Planned and managed the hardware and software upgrade of MSC USA with a 12-person team: Windows infrastructure migration from NT 4 / 2000 to 2003, Exchange 5.5 to 2003 SP1, 800+ workstations and 40 branch servers, and centralized remote management that removed the need for local IT teams."),
            ("Analicé y desarrollé planes de acción ante múltiples escenarios de desastre, incluida la destrucción total del datacenter principal, para volver a operar desde un sitio secundario en una hora.", "Analyzed and developed action plans for many disaster scenarios, including total loss of the main datacenter, to be back up from a secondary site within an hour."),
            ("Fui clave en reposicionar a la empresa como proveedor de servicios y no solo de desarrollo de software; diseñé e implementé un servicio hosteado de DRP para clientes y un “sitio remoto de desastre” para otras empresas MSC.", "Instrumental in repositioning the company as a services provider rather than just software development; designed and implemented a hosted DRP service for clients and a “remote disaster site” for other MSC companies."),
            ("Rediseñé el Help Desk tecnológico de la casa matriz y participé en el rediseño tecnológico corporativo.", "Redesigned the parent company’s technology Help Desk and took part in the corporate-wide technology redesign."),
            ("Representé a la empresa en los programas Microsoft TAP de Windows XP 64 bits, Exchange 2007 SP1, Windows Vista, 2008, 2008 R2 y 7, SQL 2005, Communicator 2005 y 2007 y Office 14.", "Represented the company in the Microsoft TAP programs for Windows XP 64-bit, Exchange 2007 SP1, Windows Vista, 2008, 2008 R2 and 7, SQL 2005, Communicator 2005 and 2007, and Office 14."),
            ("Actualización de Windows XP a Vista: creé una imagen autoconfigurable y autoactualizable para más de 1200 equipos nuevos, coordiné la imagen de fábrica con DELL, desarrollé el material de capacitación y reemplacé los más de 1200 equipos en 20 días sin pérdida de productividad.", "Windows XP to Vista upgrade: created a self-configuring, self-updating image for 1200+ new machines, coordinated factory imaging with DELL, developed the training material and replaced all 1200+ systems in 20 days with zero productivity loss."),
        ],
        photos=[],
    ),
    dict(
        slug="readers-digest", company="Reader’s Digest Argentina",
        role=t("Analista Funcional", "Functional Analyst"), period="Jun 1998 – Jul 2001",
        summary=("Reader’s Digest Argentina S.A., Buenos Aires.", "Reader’s Digest Argentina S.A., Buenos Aires."),
        resp=[
            ("Analizar y mejorar los flujos de datos de la organización", "Analyze and improve organizational data flows"),
            ("Diseñar nuevos sistemas de información y nuevas funcionalidades para los existentes", "Design new information systems and new functionality for existing systems"),
            ("Seleccionar y contratar desarrolladores y proveedores externos", "Select and hire developers and outsourcers"),
            ("Gestionar los equipos de desarrollo internos y externos", "Manage internal and external development teams"),
            ("Administración de Windows NT", "Windows NT administration"),
        ], achievements=[("Great Performers Team Award, Reader’s Digest Argentina S.A. (oct 2000)", "Great Performers Team Award, Reader’s Digest Argentina S.A. (Oct 2000)")], photos=[],
    ),
    dict(
        slug="iceberg", company="Iceberg Solutions",
        role=t("Consultor", "Consultant"), period="Mar 1997 – Jun 1998",
        summary=("Consultoría para distintos clientes, Buenos Aires.", "Consulting for several clients, Buenos Aires."),
        resp=[
            ("<b>Perez Companc S.A.</b> (sep 1997 – jun 1998) — DBA de MS-SQL (Junior DBA): administración de múltiples servidores MS-SQL, normas de seguridad de datos y estándares de desarrollo en SQL y VB 5.",
             "<b>Perez Companc S.A.</b> (Sep 1997 – Jun 1998) — MS-SQL DBA (Junior DBA): managing multiple MS-SQL servers, data security regulations and SQL / VB 5 development standards."),
            ("<b>Microsoft Consulting Services Argentina</b> (ago – sep 1997) — Desarrollador VB + MTS: aplicaciones Intranet con controles ActiveX, páginas ASP y HTML; tablas, triggers y stored procedures en SQL 6.5.",
             "<b>Microsoft Consulting Services Argentina</b> (Aug – Sep 1997) — VB + MTS developer: intranet applications with ActiveX controls, ASP and HTML pages; tables, triggers and stored procedures in SQL 6.5."),
            ("<b>Banco Río de la Plata S.A.</b> (abr – jul 1997) — Administrador / especialista Windows NT: migración de NT 3.5 a NT 4, despliegue en todas las sucursales del país, soporte de tercer nivel, control de replicación WINS, utilidades de gestión y un sistema de seguimiento de casos de HelpDesk.",
             "<b>Banco Río de la Plata S.A.</b> (Apr – Jul 1997) — Windows NT administrator / specialist: migration from NT 3.5 to NT 4, rollout in all branches across the country, 3rd-level support, WINS replication control, management utilities and a HelpDesk case-tracking system."),
        ], achievements=[], photos=[],
    ),
    dict(
        slug="ub-laboratorio", company="Universidad de Belgrano",
        role=t("Asistente de laboratorio (ad honorem) — Facultad de Tecnología Informática", "Laboratory Assistant (ad honorem) — Faculty of Information Technology"),
        period="May 1994 – Dec 1997",
        summary=("Facultad de Tecnología Informática, Universidad de Belgrano.", "Faculty of Information Technology, Universidad de Belgrano."),
        resp=[
            ("Administración y organización de las actividades diarias del laboratorio", "Administration and organization of the daily activities of the lab"),
            ("Asistencia a docentes y alumnos, capacitación y soporte técnico", "Assistance to teachers and students, training and technical support"),
            ("Administración de sistemas Windows NT, Unix y AS/400", "Administration of Windows NT, Unix and AS/400 systems"),
        ], achievements=[],
        photos=[("ub-entrada.jpg", "Frente a la entrada de la UB", ("Frente a la entrada de la Universidad de Belgrano.", "In front of the Universidad de Belgrano entrance."))],
    ),
    dict(
        slug="movicom", company="Movicom BellSouth",
        role=t("Jefe de turno de operaciones nocturnas", "Shift Manager, Night Operations"), period="Mar 1994 – Dec 1996",
        summary=("Compañía de Radiocomunicaciones Móviles S.A. (Movicom BellSouth), Buenos Aires.", "Compañía de Radiocomunicaciones Móviles S.A. (Movicom BellSouth), Buenos Aires."),
        resp=[
            ("Operación de sistemas VAX/VMS y UNIX", "System operation on VAX/VMS and UNIX"),
            ("Diseño e implementación de procedimientos operativos", "Designing and implementing operational procedures"),
            ("Desarrollo e implementación de herramientas de administración y control de procesos", "Development and implementation of tools for administration and control of processes"),
            ("Asistencia en la administración diaria de hosts y administración del paquete ALL-IN-1", "Assistance in daily host administration and administration of the ALL-IN-1 package"),
            ("Gestión del equipo del turno nocturno", "Management of the night-shift team"),
        ], achievements=[], photos=[],
    ),
    dict(
        slug="sistemas-temporarios", company="Sistemas Temporarios",
        role=t("Operador VMS — cliente: Lautrec / Saatchi &amp; Saatchi Publicidad", "VMS Operator — client: Lautrec / Saatchi &amp; Saatchi Advertising"), period="Aug 1993 – Jan 1994",
        summary=("Servicios de sistemas para una agencia de publicidad.", "Systems services for an advertising agency."),
        resp=[
            ("Administración y operación de VAX/VMS", "Administration and operations of VAX/VMS"),
            ("Administración de un host Micro-VAX 3100: usuarios, terminales, colas de impresión, módems y cuentas", "Management of a Micro-VAX 3100 host: users, terminals, print queues, modems and accounts"),
            ("Administración de una red PATHWORKS de 28 nodos (PCSA, impresión remota, transferencia de archivos, setHost)", "Administration of a 28-node PATHWORKS network (PCSA, remote printing, file transfer, setHost)"),
            ("Desarrollo en Visual Basic 1.0 y 3.0 Professional, cliente-servidor sobre RDB de Digital", "Development in Visual Basic 1.0 and 3.0 Professional, client-server over Digital RDB"),
            ("Instalación y mantenimiento de software para PC y Macintosh", "Installation and maintenance of software for PC and Macintosh"),
            ("Monitoreo del cableado y de la red de datos de fibra óptica; coordinación de capacitación", "Monitoring of cabling and the fiber-optic data network; training coordination"),
        ], achievements=[], photos=[],
    ),
    dict(
        slug="sistran", company="Sistran",
        role=t("Analista Programador", "Analyst Programmer"), period="Jul 1990 – Jul 1992",
        summary=("SISTRAN Consultores S.A., Buenos Aires.", "SISTRAN Consultores S.A., Buenos Aires."),
        resp=[
            ("Desarrollo del sistema FRUT-PACK", "Development of the FRUT-PACK system"),
            ("Desarrollo, programación y mantenimiento de sistemas para compañías de seguros, transporte y empresas frutihortícolas", "Development, programming and maintenance of systems for insurance, transport and fruit-and-vegetable companies"),
            ("Uso de UNIX, Universe y PICK sobre una amplia gama de equipos", "Using UNIX, Universe and PICK on a wide range of equipment"),
        ], achievements=[], photos=[],
    ),
]


def job_page(j):
    parts = [f'<p class="crumb"><a href="/cv.html">← {t("Experiencia", "Experience")}</a></p>',
             f"<h1>{j['company']}</h1>"]
    meta = " · ".join(x for x in [tt(j["role"]) if j["role"] else "", tt(j["period"]) if j["period"] else ""] if x)
    if meta:
        parts.append(f'<p class="lead">{meta}</p>')
    parts.append(f"<p>{tt(j['summary'])}</p>")
    for r in j.get("roles", []):
        rmeta = " · ".join(x for x in [tt(r["period"]), r["place"]] if x)
        parts.append(f"<h2>{tt(r['title'])}</h2><p class=\"meta-line\">{rmeta}</p>" + (ul(r["bullets"]) if r["bullets"] else ""))
    if j["resp"]:
        parts.append(f'<h2>{t("Responsabilidades", "Responsibilities")}</h2>{ul(j["resp"])}')
    if j["achievements"]:
        parts.append(f'<h2>{t("Logros", "Accomplishments")}</h2>{ul(j["achievements"])}')
    if j["photos"]:
        photos = [(f, a, c) for f, a, c in j["photos"]]
        parts.append(f'<h2>{t("Fotos", "Photos")}</h2>{gallery(photos)}')
    return "\n".join(parts)


# =====================================================================
# Static pages
# =====================================================================
home = f"""
<div class="hero">
  <img class="avatar" src="/assets/photo.jpg" alt="Mariano S. Cosentino">
  <div>
    <h1>Mariano S. Cosentino</h1>
    <p class="lead">{t("Apasionado por la computación y la tecnología. Buenos Aires, Argentina.",
                       "Passionate about computers and technology. Buenos Aires, Argentina.")}</p>
    <div class="links">
      {btn("https://www.linkedin.com/in/mscosentino", "linkedin", "LinkedIn", primary=True)}
      {btn("https://github.com/mok726", "github", "GitHub")}
      {btn("https://www.facebook.com/mscosentino", "facebook", "Facebook")}
      {btn("https://x.com/mok726", "x", "X")}
      {btn("https://x.com/MCTArgentina", "x", "MCT Argentina")}
      {btn("#", "mail", t("Email", "Email"), data_mail_user="mariano", data_mail_domain="mscosentino.com")}
    </div>
  </div>
</div>

<h2>{t("Sobre mí", "About me")}</h2>
<p>{t("Soy Mariano Sergio Cosentino (“Marianok” o simplemente “MOK” para mis amigos) y nací en Buenos Aires en 1971. Soy un loco de las computadoras y de la tecnología en general.",
     "I’m Mariano Sergio Cosentino (“Marianok” or simply “MOK” to my friends), and I was born in Buenos Aires, Argentina, back in ’71. I’m nuts about computers and technology in general.")}</p>
<p>{t("Empecé a jugar con computadoras a principios de los ’80. Mi primera fue una Timex Sinclair 1000, que todavía conservo: con sus 2 KB de RAM me abrió los ojos a un mundo nuevo y maravilloso.",
     "I started playing with computers in the early ’80s. My first one was a Timex Sinclair 1000 (which I still keep), and with its 2 KB of RAM it opened my eyes to a whole new world.")}</p>
<p>{t("No soy fanático de los deportes; la excepción es el buceo deportivo, una de mis pasiones. Soy una persona sencilla que disfruta de trabajar, ama los desafíos y la buena vida (sin lujos, pero con confort). Me apasiona todo lo que hago, del trabajo a los hobbies, y aunque no vivo solo el hoy, aprovecho el momento.",
     "I’m not a sports fan; the exception is scuba diving, one of my passions. I’m a simple guy who enjoys working, loves challenges and a nice life (not a luxury one). I’m passionate about everything I do, from work to hobbies, and while I don’t live only for today, I do seize the moment.")}</p>
<blockquote>{t("“Cada uno es el arquitecto de su propio destino. ¡Hacelo uno bueno!”", "“You are the architect of your own destiny. Make it a good one!”")}<cite>{t("— una frase que mi madre solía decirme", "— something my mother used to tell me")}</cite></blockquote>

<h2>{t("Desde 2015", "Since 2015")}</h2>
<ul class="timeline">
  <li><strong>{t("Hoy", "Today")}</strong><span class="meta">{t("Area Manager, Information MGT en AT&amp;T y profesor en la Universidad de Belgrano. Estudio inteligencia artificial: Claude Code in Action y AI Product Security.", "Area Manager, Information MGT at AT&amp;T and professor at Universidad de Belgrano. Studying artificial intelligence: Claude Code in Action and AI Product Security.")}</span></li>
  <li><strong>2026</strong><span class="meta">{t("El 1 de enero termina mi etapa como MCT independiente, que empezó en 1999.", "On 1 January my independent MCT career, which began in 1999, comes to an end.")}</span></li>
  <li><strong>2023 – 2025</strong><span class="meta">{t("AT&amp;T Believes Impact Award (Community Leader) tres años seguidos; en 2023 también Voluntario del Año.", "AT&amp;T Believes Impact Award (Community Leader) three years in a row; also Volunteer of the Year in 2023.")}</span></li>
  <li><strong>2022</strong><span class="meta">{t("AT&amp;T Global Volunteer Award, en voluntariado y servicios a la comunidad.", "AT&amp;T Global Volunteer Award, for volunteering and community services.")}</span></li>
  <li><strong>2021</strong><span class="meta">{t("Profesor en la Universidad de Belgrano (abril) y Area Manager, Information MGT en AT&amp;T (agosto).", "Professor at Universidad de Belgrano (April) and Area Manager, Information MGT at AT&amp;T (August).")}</span></li>
  <li><strong>2021</strong><span class="meta">{t("Paso a ser scout y asistente de liderazgo en la manada “Lobos Audaces”, donde soy Kotick.", "I become a scout and leadership assistant in the “Lobos Audaces” cub pack, where I am Kotick.")}</span></li>
  <li><strong>2019</strong><span class="meta">{t("Microsoft MCT 20th Anniversary Award. En noviembre termina mi rol como MCT Regional Lead.", "Microsoft MCT 20th Anniversary Award. My MCT Regional Lead role ends in November.")}</span></li>
  <li><strong>2018</strong><span class="meta">{t("Empiezo como voluntario en la Comunidad Scout-Guía “San Pablo”.", "I start volunteering with the Scout-Guía “San Pablo” community.")}</span></li>
  <li><strong>2016</strong><span class="meta">{t("Empiezo en AT&amp;T (abril) y como profesor adjunto en la Universidad de Belgrano (marzo). Charter Member de las nuevas certificaciones Microsoft: MCSA Web Applications, MCSD App Builder y MCSE Cloud Platform and Infrastructure.", "I join AT&amp;T (April) and the Universidad de Belgrano as adjunct professor (March). Charter Member of the new Microsoft certifications: MCSA Web Applications, MCSD App Builder and MCSE Cloud Platform and Infrastructure.")}</span></li>
  <li><strong>2015</strong><span class="meta">{t("Proctor de los Hands-On Labs en Microsoft Ignite NA (Chicago).", "Proctor for the Hands-On Labs at Microsoft Ignite NA (Chicago).")}</span></li>
</ul>

<div class="cards">
  {card("/cv.html", "work", t("Experiencia", "Experience"), t("Trabajos, estudios y reconocimientos.", "Jobs, education and recognitions."))}
  {card("/projects.html", "code", t("Proyectos", "Projects"), t("TiVo AR, XMLTV y otros desarrollos.", "TiVo AR, XMLTV and other developments."))}
  {card("/courses.html", "school", t("Cursos", "Courses"), t("Cursos y seminarios que hice.", "Courses and seminars I took."))}
  {card("/certifications.html", "verified", t("Certificaciones", "Certifications"), t("Credenciales Microsoft.", "Microsoft credentials."))}
  {card("/events.html", "event", t("Eventos", "Events"), t("Eventos y conferencias.", "Events and conferences."))}
  {card("/scout.html", "scout", "Scout", t("Mi voluntariado en la comunidad Scout.", "My volunteering in the Scout community."))}
</div>
"""

jobs_list = "".join(
    f'<li><a class="joblink" href="/jobs/{j["slug"]}.html"><strong>{j["company"]}</strong>'
    + (f'<span class="meta">{" · ".join(x for x in [tt(j["role"]) if j["role"] else "", tt(j["period"]) if j["period"] else ""] if x)}</span>' if (j["role"] or j["period"]) else "")
    + f'<span class="more">{t("Ver detalle", "See details")} →</span></a></li>'
    for j in JOBS
)

cv = f"""
<h1>{t("Experiencia", "Experience")}</h1>
<p class="lead">{t("Cada puesto tiene su propia página con responsabilidades, logros y fotos.", "Each position has its own page with responsibilities, accomplishments and photos.")}</p>

<h2>{t("Trayectoria laboral", "Work history")}</h2>
<ul class="timeline">{jobs_list}</ul>

<h2>{t("Estudios", "Education")}</h2>
{ul([
    ("California Coast University — Master of Science in IT Management (desde 2008; Summa Cum Laude, 2014)", "California Coast University — Master of Science in IT Management (from 2008; Summa Cum Laude, 2014)"),
    ("Universidad de Belgrano — Ingeniería en Computación (1994–1998)", "Universidad de Belgrano — Computer Engineering (1994–1998)"),
    ("Universidad de Belgrano — Analista de Sistemas (1994–1997)", "Universidad de Belgrano — Systems Analyst (1994–1997)"),
    ("Co.NET — Analista de Sistemas, programador BASIC y COBOL (1988–1990)", "Co.NET — Systems Analyst, BASIC and COBOL programmer (1988–1990)"),
    ("Colegio Mariano Moreno — Ciencias Físico-Matemáticas (1986–1989)", "Colegio Mariano Moreno — Physics and Mathematics (1986–1989)"),
])}

<h2>{t("Reconocimientos", "Recognitions")}</h2>
{ul(["AT&amp;T Believes Impact Award — Community Leader (2023, 2024, 2025)", "AT&amp;T Global Volunteer Award (2022)", "Microsoft MCT 20th Anniversary Award (2019)"])}

<h2>{t("Idiomas", "Languages")}</h2>
<p>{t("Español (nativo), inglés (bilingüe), italiano (básico).", "Spanish (native), English (bilingual), Italian (basic).")}</p>
"""

projects = f"""
<h1>{t("Proyectos", "Projects")}</h1>
<p class="lead">{t("Algunos desarrollos propios y contribuciones.", "Some of my own developments and contributions.")}</p>

<div class="cards">
  <div class="card">{icon("code")}<h3>TiVo AR <small>(2005–2019)</small></h3><p>{t("Adaptación de equipos TiVo de Estados Unidos para funcionar en Argentina.", "Adapting US TiVo units to work in Argentina.")}</p></div>
  <div class="card">{icon("code")}<h3>XMLTV · TV_GRAB_AR <small>(2007–2019)</small></h3><p>{t("Mantenimiento de los módulos de XMLTV para la grilla de TV argentina.", "Maintenance of the XMLTV modules for Argentine TV listings.")}</p></div>
  <a class="card" href="https://github.com/mok726/Convert-Registry-files-.reg-into-ADMX-ADML-files-for-GPO">{icon("github")}<h3>REG_2_ADMX</h3><p>{t("Convierte archivos .reg en plantillas ADMX/ADML para GPO (VBScript).", "Converts .reg files into ADMX/ADML templates for GPO (VBScript).")}</p></a>
</div>

<h2>{t("Otros desarrollos", "Other developments")}</h2>
<p>
  <span class="tag">Add-URL2URLSET</span><span class="tag">Blog Replicator</span><span class="tag">SEND2BEEPER</span>
  <span class="tag">ACD</span><span class="tag">SACE</span><span class="tag">MAP_95 / MAP_9x</span>
</p>

<h2>{t("En GitHub", "On GitHub")}</h2>
<ul class="plain">
  <li><a href="https://github.com/mok726/MMM-PictureRotator">MMM-PictureRotator</a> — {t("módulo de MagicMirror que rota imágenes de distintas fuentes", "MagicMirror module that rotates images from several sources")}</li>
  <li><a href="https://github.com/mok726/MMM-NetworkScanner">MMM-NetworkScanner</a> — {t("fork; estado de dispositivos de red por MAC", "fork; network device presence by MAC address")}</li>
  <li><a href="https://github.com/mok726/ManagedPasswordFilter">ManagedPasswordFilter</a> — {t("fork; filtro de contraseñas de Windows en código administrado", "fork; Windows password filter in managed code")}</li>
</ul>
<p class="links">{btn("https://github.com/mok726", "github", t("Ver todos en GitHub", "See all on GitHub"))}</p>
"""

COURSES_RECENT = [
    "Claude Code in Action", "AI Product Security",
    ("Agile y gestión de proyectos", "Agile and project management"),
    ("Administración de negocios", "Business administration"),
    ("OpenStack y computación en la nube", "OpenStack and cloud computing"),
    ("Privacidad y seguridad de la información", "Privacy and information security"),
    ("Licencias de software libre", "Free software licensing"),
]
COURSES_HIST = [
    ("Jun 2006", "EMC Corporation, Summit NJ", "EMC Centera Operations"),
    ("Dic 2003", "Unisys Corporation, Chicago IL", ("Workshop: “Implementing and Supporting Self-Managing Technologies in the Data Center”", "Workshop: “Implementing and Supporting Self-Managing Technologies in the Data Center”")),
    ("Dic 1997", "Sonda Computación S.A. (dictado por personal de Microsoft)", "Exchange Server 5.5"),
    ("Nov 1997", "Universidad de Belgrano", ("Planeamiento Estratégico", "Strategic Planning")),
    ("Oct 1997", "Universidad de Belgrano", ("Relevamiento Técnico", "Technical Survey")),
    ("Oct 1997", "Tecnoda S.A. (personal de Tango/04)", ("Replicación con DataMirror", "Replication with DataMirror")),
    ("Jul–Sep 1997", "Universidad de Belgrano (docentes de IT College)", "Windows NT 4.0"),
    ("Mar 1997", "IT College", ("Migrando a Windows NT 4.0", "Migrating to Windows NT 4.0")),
    ("May 1996", "Universidad de Belgrano (expertos de Siemens)", ("Seguridad de la Información", "Information Security")),
    ("Abr 1996", "Sheraton Hotel, Buenos Aires (dictado por Nicholas Negroponte)", ("Presente, pasado y futuro de Internet", "Present, Past and Future of the Internet")),
    ("Jun 1995", "Universidad de Belgrano", ("Tendencias prospectivas en computación", "Prospective Trends in Computing")),
    ("Oct 1992", "Microsoft Seminar Series, Chicago IL", "MS-Word for Windows · MS-Excel · Programming with Visual BASIC"),
    ("Jul 1992", "Joliet Junior College, Joliet IL", ("Administración de sistemas UNIX", "UNIX Systems Administration")),
    ("May 1992", "Comdex Spring ’92", ("Seguridad de datos · Algoritmos de compresión de datos y LHZ", "Data Security · Data Compression Algorithms and LHZ")),
    ("Feb 1992", "Software Development ’92", ("Multimedia: especificaciones y certificación · Capacitación con multimedia", "Multimedia: Specifications &amp; Certification · Training with Multimedia")),
    ("Feb 1989", "Instituto de PsicoOrientología", "Silva Mind Control"),
    ("", ("Otros", "Others"), ("Seguridad electrónica · Programación con Visual BASIC · Windows NT 4.0 Core Technologies", "Electronic Security · Programming with Visual BASIC · Windows NT 4.0 Core Technologies")),
]
hist = "".join(
    f'<li><strong>{tt(title)}</strong><span class="meta">{" · ".join(x for x in [d, tt(org)] if x)}</span></li>'
    for d, org, title in COURSES_HIST
)
courses = f"""
<h1>{t("Cursos y seminarios", "Courses and seminars")}</h1>
<p class="lead">{t("Formación continua a lo largo de los años.", "Continuing education over the years.")}</p>
<h2>{t("Recientes", "Recent")}</h2>
{ul(COURSES_RECENT)}
<h2>{t("Historial", "History")}</h2>
<ul class="timeline">{hist}</ul>
"""

CERTS = [
    ("Microsoft Certified Trainer (MCT)", ["Microsoft Certified Trainer"]),
    ("Microsoft Certified Solutions Expert (MCSE) — Private Cloud", ["Private Cloud"]),
    ("Microsoft Certified Solutions Developer (MCSD) 2013", ["Web Applications"]),
    ("Microsoft Certified Solutions Associate (MCSA)", ["Windows Server 2008", "Windows 7", "Windows Server 2012", "Windows 8"]),
    ("Microsoft Certified IT Professional (MCITP)", ["Enterprise Support Technician on Windows Vista", "Enterprise Desktop Support Technician on Windows 7", "Enterprise Administrator on Windows Server 2008", "Enterprise Messaging Administrator on Exchange 2007", "Enterprise Desktop Administrator on Windows 7"]),
    ("Microsoft Certified Technology Specialist (MCTS)", ["Windows Vista, Configuration", "Windows Server 2008 Active Directory, Configuration", "Windows Server 2008 Applications Infrastructure, Configuration", "Windows Server 2008 Network Infrastructure, Configuration", "Windows 7, Configuration", "Exchange Server 2007, Configuration", "Exchange Server 2010, Configuration", "SQL Server 2008, Database Development", "Dynamics CRM 2011 Extending", "Project 2010, Managing Projects", "Dynamics Retail Management System 2.0 Store Operations", "Dynamics Retail Management System 2.0 Headquarters"]),
    ("Microsoft Specialist", ["Programming in HTML5 with JavaScript and CSS3", "Programming in C#", "Administering Office 365 for Small Business", "Dynamics Deployment in CRM 2013", "Dynamics NAV 2013 Installation and Configuration", "Dynamics AX 2012 Development Introduction", "Dynamics AX 2012 Financials", "Dynamics AX 2012 Installation and Configuration"]),
    ("Microsoft Certified Dynamics Specialist", ["Dynamics AX 2012 Development Introduction", "Dynamics AX 2012 Financials", "Dynamics AX 2012 Installation and Configuration"]),
    ("Microsoft Technology Associate (MTA)", ["Software Testing Fundamentals", "Networking Fundamentals", "Security Fundamentals", "Windows Server Administration Fundamentals", "Database Fundamentals", ".NET Fundamentals", "Web Development Fundamentals", "Software Development Fundamentals", "Windows Operating System Fundamentals", "HTML5 Application Development Fundamentals"]),
    ("Microsoft Certified Systems Engineer (MCSE)", ["Windows Server 2003", "Windows 2000", "Windows NT 4.0"]),
    ("MCSE: Messaging", ["Windows 2000", "Windows Server 2003"]),
    ("MCSE: Security", ["Windows 2000", "Windows Server 2003"]),
    ("Microsoft Certified Systems Administrator (MCSA)", ["Windows Server 2003", "Windows 2000"]),
    ("MCSA: Messaging", ["Windows 2000", "Windows Server 2003"]),
    ("MCSA: Security", ["Windows Server 2003"]),
    ("Microsoft Certified Database Administrator (MCDBA)", ["SQL Server 2000"]),
    ("Microsoft Certified Solution Developer (MCSD)", [".NET", "Visual Studio 6.0"]),
    ("MCSD — Windows Architecture (old track)", ["Windows Architecture I", "Windows Architecture II"]),
    ("Microsoft Certified Application Developer (MCAD)", [".NET"]),
    ("Microsoft Certified Desktop Support Technician (MCDST)", ["Windows XP"]),
]
cert_html = "".join(
    f'<details class="cert"><summary>{name}</summary><p>' + "".join(f'<span class="tag">{i}</span>' for i in items) + "</p></details>"
    for name, items in CERTS
)
certs = f"""
<h1>{t("Certificaciones", "Certifications")}</h1>
<p class="lead">{t("Certificaciones Microsoft obtenidas a lo largo de mi carrera. Algunas corresponden a programas ya retirados.", "Microsoft certifications earned throughout my career. Some belong to programs that have since been retired.")}</p>
<p><a href="https://mcp.microsoft.com/authenticate/validatemcp.aspx">{t("Verificación en el sitio de Microsoft", "Verify on the Microsoft site")} →</a></p>
{cert_html}
"""

events = f"""
<h1>{t("Eventos y conferencias", "Events and conferences")}</h1>
<p class="lead">{t("Eventos que organicé o en los que participé.", "Events I organized or took part in.")}</p>
<ul class="timeline">
  <li><strong>Microsoft Ignite NA 2015 — HOL Proctor</strong><span class="meta">{t("2015 – actualidad · Voluntario", "2015 – present · Volunteer")}</span>
    <p>{t("Proctor de los laboratorios prácticos (Hands-On Labs).", "Proctor for the Hands-On Labs.")}</p></li>
  <li><strong>COMDEX / Windows World / Infocomm Argentina 1998</strong><span class="meta">{t("18 al 22 de mayo de 1998 · Predio Rural de Palermo · Orador", "18–22 May 1998 · Predio Rural de Palermo · Speaker")}</span>
    <p>{t("Tema: Microsoft Transaction Server. Organizado por Microsoft Argentina S.A.", "Topic: Microsoft Transaction Server. Hosted by Microsoft Argentina S.A.")}</p></li>
  <li><strong>“Tecnología en Papel” — {t("primera exposición de publicaciones informáticas", "first exhibition of computer publications")}</strong><span class="meta">{t("24 al 26 de octubre de 1994 · José Hernández 1880, Capital Federal · Organizó la Facultad de Tecnología Informática, Universidad de Belgrano", "24–26 October 1994 · José Hernández 1880, Capital Federal · Sponsored by the Faculty of Information Technology, Universidad de Belgrano")}</span>
    {ul([("Selección de las empresas expositoras", "Selection of exhibitor companies"), ("Selección y preparación del espacio físico", "Selection and preparation of the physical space"), ("Publicidad y relaciones públicas de la muestra", "Advertising and public relations of the exhibition")])}</li>
</ul>
"""

scout = f"""
<h1>Scout</h1>
<p class="lead">{t("Voluntariado en la Comunidad Scout-Guía “San Pablo”, Scouts de Argentina.", "Volunteering with the Scout-Guía “San Pablo” community, Scouts de Argentina.")}</p>
<p>{t("Soy asistente de liderazgo en la manada “Lobos Audaces”, donde mi nombre de caza es <strong>Kotick</strong>. Empecé como padre ayudante en 2018 y desde octubre de 2021 soy scout.",
     "I am a leadership assistant in the “Lobos Audaces” cub pack, where my hunting name is <strong>Kotick</strong>. I started as a parent helper in 2018 and have been a scout since October 2021.")}</p>
<h2>{t("Recorrido", "Path")}</h2>
<ul class="timeline">
  <li><strong>{t("Scout — asistente de liderazgo, manada “Lobos Audaces”", "Scout — leadership assistant, “Lobos Audaces” pack")}</strong><span class="meta">{t("Oct 2021 – actualidad", "Oct 2021 – present")}</span></li>
  <li><strong>{t("Padre ayudante / adulto ayudante", "Parent helper / adult helper")}</strong><span class="meta">Mar 2018 – Oct 2021</span></li>
</ul>
<h2>{t("Reconocimientos", "Recognitions")}</h2>
{ul([("AT&amp;T Believes Impact Award — Community Leader (2023, 2024 y 2025); en 2023 también Voluntario del Año", "AT&amp;T Believes Impact Award — Community Leader (2023, 2024 and 2025); Volunteer of the Year in 2023"), "AT&amp;T Global Volunteer Award (2022)"])}
<h2>{t("Fotos", "Photos")}</h2>
{gallery([
    ("scout-manada.jpg", "Saludo scout con el uniforme de Educador de Manada", ("Kotick, Educador de Manada.", "Kotick, cub pack educator.")),
    ("scout-30-anios.jpg", "Junto al cartel de los 30 años de Scouts de Argentina, Zona 15", ("30 años de Scouts de Argentina — Zona 15.", "30 years of Scouts de Argentina — Zone 15.")),
])}
"""

PAGES = [
    ("index.html", "index.html", "Inicio", "Mariano S. Cosentino — tecnología, nube y docencia.", "Mariano S. Cosentino — technology, cloud and teaching.", home),
    ("cv.html", "cv.html", "Experiencia", "Trayectoria, estudios y reconocimientos.", "Career, education and recognitions.", cv),
    ("projects.html", "projects.html", "Proyectos", "Proyectos y desarrollos.", "Projects and developments.", projects),
    ("courses.html", "courses.html", "Cursos", "Cursos y seminarios realizados.", "Courses and seminars taken.", courses),
    ("certifications.html", "certifications.html", "Certificaciones", "Certificaciones Microsoft.", "Microsoft certifications.", certs),
    ("events.html", "events.html", "Eventos", "Eventos y conferencias.", "Events and conferences.", events),
    ("scout.html", "scout.html", "Scout", "Voluntariado Scout.", "Scout volunteering.", scout),
]

os.makedirs(os.path.join(OUT, "jobs"), exist_ok=True)
for path, cur, title, des, den, body in PAGES:
    with open(os.path.join(OUT, path), "w", encoding="utf8") as fh:
        fh.write(page(path, cur, title, des, den, body))
for j in JOBS:
    name = j["company"].replace("&amp;", "&")
    with open(os.path.join(OUT, "jobs", j["slug"] + ".html"), "w", encoding="utf8") as fh:
        fh.write(page(f"jobs/{j['slug']}.html", "cv.html", name, f"{name} — experiencia laboral.", f"{name} — work experience.", job_page(j)))
print("ok", len(PAGES) + len(JOBS), "pages")
