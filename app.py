import os
import json
import time
import hmac
import secrets
import logging
from datetime import datetime, timezone

from markdown import markdown as _md_to_html
from bson.objectid import ObjectId
import bcrypt as _bcrypt
import bleach
from motor.motor_asyncio import AsyncIOMotorClient
from fenrir import Fenrir, render_template, session
from fenrir.response import RedirectResponse

logger = logging.getLogger(__name__)

BLEACH_ALLOWED_TAGS = [
    "p", "br", "b", "i", "em", "strong", "a", "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "h5", "h6", "code", "pre", "blockquote",
    "hr", "table", "thead", "tbody", "tr", "th", "td", "img",
    "span", "div",
]
BLEACH_ALLOWED_ATTRS = {
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title", "width", "height", "loading"],
    "code": ["class"],
    "pre": ["class"],
    "span": ["class"],
    "div": ["class"],
    "td": ["colspan", "rowspan"],
    "th": ["colspan", "rowspan"],
}
BLEACH_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

app = Fenrir(
    title="IshikawaUta Portfolio",
    version="1.0.0",
    template_folder="templates",
)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "uta-home-secret-key-change-in-production"
)
_is_secure = bool(os.environ.get("VERCEL")) or bool(os.environ.get("DOCKER"))
app.config["SESSION_COOKIE_SECURE"] = _is_secure
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# GZip compression (skip in Vercel/Docker - handled upstream)
if not os.environ.get("VERCEL") and not os.environ.get("DOCKER"):
    from fenrir.middleware import GZipMiddleware
    app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=6)

# Serve static files (skip in Vercel - serves from public/ automatically)
if not os.environ.get("VERCEL"):
    from fenrir.static import StaticFiles
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")))

# Load .env file in development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# MongoDB connection
# ---------------------------------------------------------------------------
mongo_client = None
mongo_db = None

async def get_mongo_db():
    global mongo_client, mongo_db
    if mongo_db is not None:
        return mongo_db
    uri = os.environ.get("MONGODB_URI")
    if not uri:
        return None
    try:
        mongo_client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        await mongo_client.admin.command("ping")
        mongo_db = mongo_client.get_database("uta-home")
        return mongo_db
    except Exception:
        return None


async def _db_or_fail():
    db = await get_mongo_db()
    if db is None:
        raise RuntimeError("MongoDB tidak terhubung")
    return db

async def mongo_is_connected():
    return (await get_mongo_db()) is not None

# ---------------------------------------------------------------------------
# Profile data - hardcoded fallback
# ---------------------------------------------------------------------------
PROFILE = {
    "name": "Eka Saputra",
    "alias": "ishikawauta",
    "tagline": "Full Stack Developer / Software Developer / Open Source Enthusiast",
    "codeFile": "app.py",
    "avatarUrl": "https://avatars.githubusercontent.com/u/79686853?v=4",
    "copyright": "\u00a9 2026-present @IshikawaUta. All rights reserved.",
    "about": [
        "Full Stack Developer passionate about open source. Building various projects from web frameworks (Fenrir) to inventory management systems.",
        "Creator of Fenrir Framework - Python ASGI web framework, Asteri Server - Python ASGI web server, and various other open source projects.",
    ],
    "tags": [
        {"year": "'21", "label": "Open Source"},
        {"year": "'22", "label": "Python"},
        {"year": "'23", "label": "Fenrir"},
        {"year": "'24", "label": "Asteri"},
        {"year": "'25", "label": "Flask"},
        {"year": "'26", "label": "More to come..."},
    ],
    "techStack": {
        "innerIcons": ["python", "js", "ruby", "php", "html"],
        "outerIcons": ["rails", "django", "next", "flask", "nodejs", "laravel", "tailwind", "css", "git"],
    },
    "socialLinks": [
        {"label": "GitHub", "href": "https://github.com/IshikawaUta"},
        {"label": "Blog", "href": "https://ishikawauta.github.io/my-blogs"},
        {"label": "Mail", "href": "mailto:komikers09@gmail.com"},
    ],
    "achievements": [
        {"title": "Fenrir Framework", "description": "High-performance Python ASGI web framework", "year": "1.5k Stars"},
        {"title": "Asteri Server", "description": "High-performance Python web server", "year": "1.2k Stars"},
        {"title": "Ofa Framework", "description": "Templating Ruby web framework", "year": "1k Stars"},
        {"title": "Open Source", "description": "151+ repositories and counting", "year": "Builder"},
    ],
    "projects": [
        {
            "title": "Fenrir Web Framework",
            "badges": [
                {"href": "https://pypi.org/project/fenrir-framework/", "img": "https://img.shields.io/pypi/v/fenrir-framework.svg?color=blueviolet", "alt": "PyPI version"},
                {"href": "https://opensource.org/licenses/MIT", "img": "https://img.shields.io/badge/License-MIT-blue.svg", "alt": "License: MIT"},
                {"href": "https://www.python.org/", "img": "https://img.shields.io/badge/Python-3.8%2B-blue.svg", "alt": "Python Version"},
                {"href": "https://github.com/IshikawaUta/fenrir/actions", "img": "https://img.shields.io/badge/Tests-1536%20Passed-brightgreen.svg", "alt": "Tests"},
                {"href": "https://github.com/IshikawaUta/fenrir/actions/workflows/test.yml", "img": "https://github.com/IshikawaUta/fenrir/actions/workflows/test.yml/badge.svg", "alt": "CI"},
                {"href": "", "img": "https://img.shields.io/badge/Performance-High--Speed%20ASGI-orange.svg", "alt": "Performance"},
            ],
            "description": '<strong class="text-foreground">Fenrir</strong> is a state-of-the-art, high-performance, hybrid Python web framework built on top of modern ASGI specifications. It elegantly merges the best programming paradigms from Python\'s most popular web frameworks (<strong>Flask</strong>, <strong>FastAPI</strong>, <strong>Sanic</strong>, <strong>Falcon</strong>, and <strong>Bottle</strong>) into a single unified workspace, powered locally by the premium <strong>Asteri</strong> application server.',
            "github": "https://github.com/IshikawaUta/fenrir",
            "demo": "https://fenrir.eksashop.web.id/",
        },
        {
            "title": "Asteri Web Server",
            "badges": [
                {"href": "https://pypi.org/project/asteri/", "img": "https://img.shields.io/pypi/v/asteri.svg?color=blueviolet", "alt": "PyPI version"},
                {"href": "https://opensource.org/licenses/MIT", "img": "https://img.shields.io/badge/License-MIT-blue.svg", "alt": "License: MIT"},
                {"href": "https://www.python.org/", "img": "https://img.shields.io/badge/Python-3.10%2B-blue.svg", "alt": "Python Version"},
                {"href": "https://github.com/IshikawaUta/asteri/actions", "img": "https://img.shields.io/badge/CI-Passing-brightgreen.svg", "alt": "CI"},
                {"href": "", "img": "https://img.shields.io/badge/HTTP-1.1%20%7C%202%20%7C%203%20(QUIC)-orange.svg", "alt": "Protocols"},
                {"href": "", "img": "https://img.shields.io/badge/Workers-Sync%20%7C%20GThread%20%7C%20Gevent%20%7C%20ASGI%20%7C%20Tornado-brightgreen.svg", "alt": "Workers"},
            ],
            "description": '<strong class="text-foreground">Asteri</strong> is a state-of-the-art, high-performance, production-ready Python web server with rich CLI argument system. Supports <strong>HTTP/1.1</strong>, <strong>HTTP/2</strong>, <strong>HTTP/3 (QUIC)</strong>, WSGI, ASGI, uWSGI, WebSocket, and premium event loops like <strong>Tornado</strong>. Features C-Extension core, Prometheus/OpenTelemetry metrics, proxy protocol, systemd socket activation, and a premium status dashboard.',
            "github": "https://github.com/IshikawaUta/asteri",
        },
        {
            "title": "IshikawaUta Portfolio",
            "badges": [
                {"href": "https://opensource.org/licenses/MIT", "img": "https://img.shields.io/badge/License-MIT-blue.svg", "alt": "License: MIT"},
                {"href": "https://www.python.org/", "img": "https://img.shields.io/badge/Python-3.10%2B-blue.svg", "alt": "Python Version"},
                {"href": "https://pypi.org/project/fenrir-framework/", "img": "https://img.shields.io/badge/Fenrir-Framework-9b59b6.svg", "alt": "Framework"},
                {"href": "https://github.com/IshikawaUta/Uta-Homepage/actions", "img": "https://img.shields.io/badge/Tests-116%20Passed-brightgreen.svg", "alt": "Tests"},
                {"href": "https://github.com/IshikawaUta/Uta-Homepage/actions", "img": "https://img.shields.io/badge/Coverage-100%25-brightgreen.svg", "alt": "Coverage"},
                {"href": "https://github.com/IshikawaUta/Uta-Homepage/actions/workflows/ci.yml", "img": "https://github.com/IshikawaUta/Uta-Homepage/actions/workflows/ci.yml/badge.svg", "alt": "CI"},
                {"href": "", "img": "https://img.shields.io/badge/Deployed-Vercel-black.svg", "alt": "Deployment"},
                {"href": "", "img": "https://img.shields.io/badge/Performance-High--Speed%20ASGI-orange.svg", "alt": "Performance"},
            ],
            "description": 'Portfolio website built with <strong class="text-foreground">Fenrir Framework</strong>, featuring performance-first architecture with no database dependency.',
            "github": "https://github.com/IshikawaUta/Uta-Homepage",
            "demo": "https://uta.eksashop.web.id",
        },
        {
            "title": "InventarisKu",
            "badges": [
                {"href": "https://pypi.org/project/fenrir-framework/", "img": "https://img.shields.io/badge/Fenrir-4.1.2-purple.svg", "alt": "Fenrir Framework"},
                {"href": "https://opensource.org/licenses/MIT", "img": "https://img.shields.io/badge/License-MIT-blue.svg", "alt": "License: MIT"},
                {"href": "https://www.python.org/", "img": "https://img.shields.io/badge/Python-3.12-blue.svg", "alt": "Python Version"},
                {"href": "https://github.com/IshikawaUta/stokbox-inventory-managements/actions", "img": "https://img.shields.io/badge/Tests-508%20Passed-brightgreen.svg", "alt": "Tests"},
                {"href": "https://github.com/IshikawaUta/stokbox-inventory-managements/actions/workflows/test.yml", "img": "https://github.com/IshikawaUta/stokbox-inventory-managements/actions/workflows/test.yml/badge.svg", "alt": "CI"},
                {"href": "", "img": "https://img.shields.io/badge/Coverage-93%25-brightgreen.svg", "alt": "Coverage"},
                {"href": "https://www.mongodb.com/atlas", "img": "https://img.shields.io/badge/DB-MongoDB%20Atlas-green.svg", "alt": "MongoDB"},
                {"href": "https://cloudinary.com", "img": "https://img.shields.io/badge/Storage-Cloudinary-orange.svg", "alt": "Cloudinary"},
            ],
            "description": 'Modern inventory management system built with <strong class="text-foreground">Fenrir Framework v4.1.2</strong> + <strong>MongoDB Atlas</strong>. Async Python backend, NoSQL database, Cloudinary media storage, Jinja2 + Vanilla JS frontend.',
            "github": "https://github.com/IshikawaUta/stokbox-inventory-managements",
        },
        {
            "title": "DOSStack",
            "badges": [
                {"href": "https://opensource.org/licenses/MIT", "img": "https://img.shields.io/badge/License-MIT-blue.svg", "alt": "License: MIT"},
                {"href": "", "img": "https://img.shields.io/badge/Type-Compiled%20Binary-red.svg", "alt": "Type"},
                {"href": "", "img": "https://img.shields.io/badge/Attacks-19%20Modes-brightgreen.svg", "alt": "Attacks"},
                {"href": "", "img": "https://img.shields.io/badge/Engines-Thread%20%7C%20Epoll%20%7C%20MP-blueviolet.svg", "alt": "Engines"},
                {"href": "", "img": "https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg", "alt": "Platform"},
            ],
            "description": '<strong class="text-foreground">DOSStack</strong> is a compiled DoS testing framework with 19 attack modes (HTTP, TCP, UDP, Slowloris, ICMP, TLS, Mixed, raw SYN/ACK/RST/FIN/SYNACK, IP fragmentation, and 6 amplification vectors). Features 3 engines (thread pool, epoll, multiprocessing), connection pooling, burst mode, bandwidth control, IP spoofing, proxy rotation, and real-time stats dashboard.',
            "github": "https://github.com/IshikawaUta/dosstack",
        },
    ],
}

# ---------------------------------------------------------------------------
# JSON-LD structured data for SEO (schema.org ProfilePage)
# ---------------------------------------------------------------------------
def build_jsonld(profile, site_url):
    """Build JSON-LD structured data for search engines."""
    data = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "mainEntity": {
            "@type": "Person",
            "name": profile["name"],
            "alternateName": profile["alias"],
            "url": site_url,
            "sameAs": [link["href"] for link in profile["socialLinks"]],
        },
    }
    return json.dumps(data)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_projects_cache = None
_projects_cache_ts = 0.0

async def fetch_projects():
    global _projects_cache, _projects_cache_ts
    now = time.time()
    if _projects_cache is not None and (now - _projects_cache_ts) < 60:
        return _projects_cache
    db = await get_mongo_db()
    if db is not None:
        try:
            cursor = db.projects.find().sort("order", 1)
            projects = await cursor.to_list(None)
            if projects:
                result = []
                for p in projects:
                    result.append({
                        "title": p.get("title", ""),
                        "badges": p.get("badges", []),
                        "description": bleach.clean(p.get("description", ""), tags=BLEACH_ALLOWED_TAGS, attributes=BLEACH_ALLOWED_ATTRS, protocols=BLEACH_ALLOWED_PROTOCOLS, strip=True),
                        "github": p.get("github", ""),
                        "demo": p.get("demo", ""),
                    })
                _projects_cache = result
                _projects_cache_ts = now
                return result
        except Exception:
            logger.exception("Gagal fetch projects dari MongoDB")
    return PROFILE["projects"]


SESSION_TTL = 1800

def admin_required(handler):
    """Decorator to protect admin routes with session timeout."""
    async def wrapper(req, *args, **kwargs):
        if not session.get("logged_in"):
            return RedirectResponse("/admin/login", status=302)
        login_at = session.get("_login_at", 0)
        if time.time() - login_at > SESSION_TTL:
            session.clear()
            return RedirectResponse("/admin/login?expired=1", status=302)
        path_params = getattr(req, "path_params", {})
        merged = {**path_params, **kwargs}
        return await handler(req, *args, **merged)
    return wrapper


def get_admin_credentials():
    return (
        os.environ.get("ADMIN_USERNAME", "admin"),
        os.environ.get("ADMIN_PASSWORD", "admin123"),
    )


_admin_password_hash = None

def _hash_admin_password():
    global _admin_password_hash
    if _admin_password_hash is not None:
        return _admin_password_hash
    try:
        import bcrypt as _bcrypt
        password = get_admin_credentials()[1]
        _admin_password_hash = _bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt())
    except Exception:
        _admin_password_hash = None
    return _admin_password_hash


def check_admin_password(password):
    pwhash = _hash_admin_password()
    if pwhash is None:
        return get_admin_credentials()[1] == password
    try:
        import bcrypt as _bcrypt
        return _bcrypt.checkpw(password.encode("utf-8"), pwhash)
    except Exception:
        return get_admin_credentials()[1] == password

# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@app.get("/")
async def index(req):
    """Main page - renders index.html with profile data, canonical URL, and JSON-LD."""
    scheme = "https" if req.headers.get("x-forwarded-proto") == "https" else "http"
    host = req.headers.get("host") or "127.0.0.1:8000"
    site_url = f"{scheme}://{host}/"
    canonical_url = site_url
    json_ld = build_jsonld(PROFILE, site_url)
    profile = dict(PROFILE)
    profile["projects"] = await fetch_projects()
    return render_template("index.html", profile=profile, canonical_url=canonical_url, json_ld=json_ld)


@app.get("/favicon.ico")
async def favicon(req):
    """Redirect favicon requests to GitHub avatar URL (no local favicon file)."""
    return ("", 302, {"Location": PROFILE["avatarUrl"]})


@app.get("/robots.txt")
async def robots(req):
    """Generate robots.txt dynamically with correct sitemap URL."""
    scheme = "https" if req.headers.get("x-forwarded-proto") == "https" else "http"
    host = req.headers.get("host") or "127.0.0.1:8000"
    sitemap_url = f"{scheme}://{host}/sitemap.xml"
    content = f"""User-agent: *
Allow: /
Sitemap: {sitemap_url}
"""
    return (content, 200, {"Content-Type": "text/plain"})


@app.get("/sitemap.xml")
async def sitemap(req):
    """Generate sitemap.xml dynamically with correct base URL."""
    scheme = "https" if req.headers.get("x-forwarded-proto") == "https" else "http"
    host = req.headers.get("host") or "127.0.0.1:8000"
    site_url = f"{scheme}://{host}"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>{site_url}/</loc>
      <lastmod>2026-07-02</lastmod>
      <changefreq>monthly</changefreq>
      <priority>1.0</priority>
   </url>
</urlset>
"""
    return (xml, 200, {"Content-Type": "application/xml"})

# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------

MAX_LOGIN_ATTEMPTS = 10
LOGIN_WINDOW = 900

def _check_login_rate_limit():
    attempts = session.get("_login_attempts", 0)
    window_start = session.get("_login_window", 0)
    now = time.time()
    if now - window_start > LOGIN_WINDOW:
        session["_login_attempts"] = 0
        session["_login_window"] = now
        return True
    return attempts < MAX_LOGIN_ATTEMPTS


def _generate_csrf():
    token = secrets.token_hex(32)
    session["_csrf_token"] = token
    return token


def _validate_csrf(form):
    if app.config.get("DISABLE_CSRF"):
        return True
    expected = session.pop("_csrf_token", None)
    if expected is None:
        return False
    return hmac.compare_digest(str(form.get("_csrf_token", "")), expected)


@app.get("/admin/login")
async def admin_login_get(req):
    if session.get("logged_in"):
        return RedirectResponse("/admin", status=302)
    _generate_csrf()
    return render_template("admin/login.html", csrf_token=session["_csrf_token"])


@app.post("/admin/login")
async def admin_login_post(req):
    if session.get("logged_in"):
        return RedirectResponse("/admin", status=302)
    form = await req.form()
    if not _validate_csrf(form):
        return render_template("admin/login.html", error="Session expired, coba lagi", csrf_token=_generate_csrf())
    if not _check_login_rate_limit():
        return render_template("admin/login.html", error="Terlalu banyak percobaan. Tunggu 15 menit.", csrf_token=_generate_csrf())
    username = form.get("username", "")
    password = form.get("password", "")
    expected_user, expected_pass = get_admin_credentials()
    if hmac.compare_digest(username, expected_user) and check_admin_password(password):
        session["logged_in"] = True
        session["_login_at"] = time.time()
        session.pop("_login_attempts", None)
        session.pop("_login_window", None)
        return RedirectResponse("/admin", status=302)
    session["_login_attempts"] = session.get("_login_attempts", 0) + 1
    if session["_login_attempts"] == 1:
        session["_login_window"] = time.time()
    return render_template("admin/login.html", error="Username atau password salah", csrf_token=_generate_csrf())


@app.get("/admin/logout")
async def admin_logout(req):
    session.pop("logged_in", None)
    return RedirectResponse("/admin/login", status=302)


@app.get("/admin")
@admin_required
async def admin_dashboard(req):
    connected = await mongo_is_connected()
    projects = []
    if connected:
        try:
            db = await _db_or_fail()
            cursor = db.projects.find().sort("order", 1)
            projects = await cursor.to_list(None)
            for p in projects:
                p["_id"] = str(p["_id"])
                p.pop("created_at", None)
                p.pop("updated_at", None)
        except Exception:
            connected = False
    return render_template(
        "admin/dashboard.html",
        mongo_connected=connected,
        projects=projects,
        csrf_token=_generate_csrf(),
    )


@app.get("/admin/projects/new")
@admin_required
async def admin_project_new_get(req):
    if not await mongo_is_connected():
        return render_template("admin/dashboard.html", mongo_connected=False, projects=[], error="MongoDB tidak terhubung", csrf_token=_generate_csrf())
    return render_template("admin/projects/form.html", project=None, badges_json="", csrf_token=_generate_csrf())


@app.post("/admin/projects")
@admin_required
async def admin_project_create(req):
    if not await mongo_is_connected():
        return render_template("admin/dashboard.html", mongo_connected=False, projects=[], error="MongoDB tidak terhubung", csrf_token=_generate_csrf())
    form = await req.form()
    if not _validate_csrf(form):
        return render_template("admin/dashboard.html", mongo_connected=True, projects=[], error="CSRF token invalid", csrf_token=_generate_csrf())
    error = validate_project_form(form)
    if error:
        return render_template("admin/projects/form.html", project=None, error=error, badges_json=form.get("badges", ""), csrf_token=_generate_csrf())
    try:
        db = await _db_or_fail()
        doc = build_project_doc(form)
        await db.projects.insert_one(doc)
        _projects_cache = None
        return RedirectResponse("/admin?success=Project berhasil ditambahkan", status=302)
    except Exception as e:
        return render_template("admin/projects/form.html", project=None, error=f"Gagal menyimpan: {str(e)}", badges_json=form.get("badges", ""), csrf_token=_generate_csrf())


@app.get("/admin/projects/<id>/edit")
@admin_required
async def admin_project_edit_get(req, id):
    if not await mongo_is_connected():
        return render_template("admin/dashboard.html", mongo_connected=False, projects=[], error="MongoDB tidak terhubung", csrf_token=_generate_csrf())
    try:
        db = await _db_or_fail()
        project = await db.projects.find_one({"_id": ObjectId(id)})
        if not project:
            return render_template("admin/dashboard.html", mongo_connected=True, projects=[], error="Project tidak ditemukan", csrf_token=_generate_csrf())
        project["_id"] = str(project["_id"])
        project["description"] = project.get("description_raw") or project.get("description", "")
        badges_json = json.dumps(project.get("badges", []), indent=2)
        return render_template("admin/projects/form.html", project=project, badges_json=badges_json, csrf_token=_generate_csrf())
    except Exception as e:
        return render_template("admin/dashboard.html", mongo_connected=True, projects=[], error=f"Error: {str(e)}", csrf_token=_generate_csrf())


@app.post("/admin/projects/<id>")
@admin_required
async def admin_project_update(req, id):
    if not await mongo_is_connected():
        return render_template("admin/dashboard.html", mongo_connected=False, projects=[], error="MongoDB tidak terhubung", csrf_token=_generate_csrf())
    form = await req.form()
    if not _validate_csrf(form):
        return render_template("admin/dashboard.html", mongo_connected=True, projects=[], error="CSRF token invalid", csrf_token=_generate_csrf())
    error = validate_project_form(form)
    if error:
        badges_json = form.get("badges", "")
        return render_template("admin/projects/form.html", project={"_id": id, **form}, error=error, badges_json=badges_json, csrf_token=_generate_csrf())
    try:
        db = await _db_or_fail()
        doc = build_project_doc(form)
        doc["updated_at"] = datetime.now(timezone.utc)
        await db.projects.update_one({"_id": ObjectId(id)}, {"$set": doc})
        _projects_cache = None
        return RedirectResponse("/admin?success=Project berhasil diupdate", status=302)
    except Exception as e:
        return render_template("admin/projects/form.html", project={"_id": id, **form}, error=f"Gagal update: {str(e)}", badges_json=form.get("badges", ""), csrf_token=_generate_csrf())


@app.post("/admin/projects/<id>/delete")
@admin_required
async def admin_project_delete(req, id):
    if not await mongo_is_connected():
        return render_template("admin/dashboard.html", mongo_connected=False, projects=[], error="MongoDB tidak terhubung", csrf_token=_generate_csrf())
    form = await req.form()
    if not _validate_csrf(form):
        return render_template("admin/dashboard.html", mongo_connected=True, projects=[], error="CSRF token invalid", csrf_token=_generate_csrf())
    try:
        db = await _db_or_fail()
        await db.projects.delete_one({"_id": ObjectId(id)})
        _projects_cache = None
        return RedirectResponse("/admin?success=Project berhasil dihapus", status=302)
    except Exception as e:
        cursor = db.projects.find()
        remaining = await cursor.to_list(None)
        return render_template("admin/dashboard.html", mongo_connected=True, projects=remaining, error=f"Gagal hapus: {str(e)}", csrf_token=_generate_csrf())


def validate_project_form(form):
    if not form.get("title", "").strip():
        return "Title wajib diisi"
    return None


def md_to_html(text):
    html = _md_to_html(text or "", extensions=["fenced_code", "codehilite"])
    return bleach.clean(
        html,
        tags=BLEACH_ALLOWED_TAGS,
        attributes=BLEACH_ALLOWED_ATTRS,
        protocols=BLEACH_ALLOWED_PROTOCOLS,
        strip=True,
    )


def build_project_doc(form):
    now = datetime.now(timezone.utc)
    badges = []
    raw_badges = form.get("badges", "").strip()
    if raw_badges:
        try:
            badges = json.loads(raw_badges)
            if not isinstance(badges, list):
                badges = []
        except json.JSONDecodeError:
            badges = []
    raw_description = form.get("description", "").strip()
    converted = md_to_html(raw_description) if raw_description else ""
    return {
        "title": form.get("title", "").strip(),
        "description": converted,
        "description_raw": raw_description or converted,
        "github": form.get("github", "").strip(),
        "demo": form.get("demo", "").strip(),
        "badges": badges,
        "order": int(form.get("order", 0)),
        "created_at": now,
        "updated_at": now,
    }

# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.exception(404)
async def not_found(req, exc):
    """Handle 404 errors - render custom error page."""
    return render_template("error.html", status=404, message="Page not found", profile=PROFILE), 404


@app.exception(500)
async def server_error(req, exc):
    """Handle 500 errors - render custom error page."""
    return render_template("error.html", status=500, message="Internal server error", profile=PROFILE), 500


if __name__ == "__main__":  # pragma: no cover
    app.run()
