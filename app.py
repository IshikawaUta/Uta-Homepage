# =============================================================================
# IshikawaUta Portfolio - Fenrir Web Framework
# =============================================================================
# Entry point for the portfolio website. All profile data is hardcoded
# (no database). Built with Fenrir Framework + Asteri ASGI server.
#
# Local:  fenrir run app:app --host 0.0.0.0 --port 8000
# Dev:    fenrir run app:app --dev
# Vercel: Automatic (api/index.py imports this app)
# =============================================================================

import os
import json
from fenrir import Fenrir, render_template

# ---------------------------------------------------------------------------
# App initialization
# ---------------------------------------------------------------------------
app = Fenrir(
    title="IshikawaUta Portfolio",
    version="1.0.0",
    template_folder="templates",
)

# GZip compression (only for local/production, not Vercel which handles it)
if not os.environ.get("VERCEL"):
    from fenrir.middleware import GZipMiddleware
    app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=6)

    # Serve static files locally (Vercel serves from public/ automatically)
    from fenrir.static import StaticFiles
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")))

# ---------------------------------------------------------------------------
# Profile data - hardcoded, no database needed
# ---------------------------------------------------------------------------
PROFILE = {
    "name": "Eka Saputra",
    "alias": "ishikawauta",
    "tagline": "Full Stack Developer / Software Developer / Open Source Enthusiast",
    "codeFile": "app.py",                       # Filename shown in code preview
    "avatarUrl": "https://avatars.githubusercontent.com/u/79686853?v=4",
    "copyright": "\u00a9 2026-present @IshikawaUta. All rights reserved.",
    # About paragraphs (rendered as <p> tags in About section)
    "about": [
        "Full Stack Developer passionate about open source. Building various projects from web frameworks (Fenrir) to inventory management systems.",
        "Creator of Fenrir Framework - Python ASGI web framework, Asteri Server - Python ASGI web server, and various other open source projects.",
    ],
    # Timeline tags displayed under About Me section
    "tags": [
        {"year": "'21", "label": "Open Source"},
        {"year": "'22", "label": "Python"},
        {"year": "'23", "label": "Fenrir"},
        {"year": "'24", "label": "Asteri"},
        {"year": "'25", "label": "Flask"},
        {"year": "'26", "label": "More to come..."},
    ],
    # Tech stack icons for orbiting circles (uses skillicons.dev API)
    "techStack": {
        "innerIcons": ["python", "js", "ruby", "php", "html"],      # Inner orbit (smaller)
        "outerIcons": ["rails", "django", "next", "flask", "nodejs", "laravel", "tailwind", "css", "git"],  # Outer orbit (larger)
    },
    # Social links rendered in header navigation
    "socialLinks": [
        {"label": "GitHub", "href": "https://github.com/IshikawaUta"},
        {"label": "Blog", "href": "https://ishikawauta.github.io/my-blogs"},
        {"label": "Mail", "href": "mailto:komikers09@gmail.com"},
    ],
    # Achievement cards shown in right column
    "achievements": [
        {"title": "Fenrir Framework", "description": "High-performance Python ASGI web framework", "year": "1.5k Stars"},
        {"title": "Asteri Server", "description": "High-performance Python web server", "year": "1.2k Stars"},
        {"title": "Ofa Framework", "description": "Templating Ruby web framework", "year": "1k Stars"},
        {"title": "Open Source", "description": "151+ repositories and counting", "year": "Builder"},
    ],
    # Project experience cards with pagination
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
            "description": 'Sistem manajemen inventaris barang modern berbasis <strong class="text-foreground">Fenrir Framework v4.1.2</strong> + <strong>MongoDB Atlas</strong>. Backend async Python, database NoSQL, media storage via Cloudinary, frontend Jinja2 + Vanilla JS.',
            "github": "https://github.com/IshikawaUta/stokbox-inventory-managements",
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
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
async def index(req):
    """Main page - renders index.html with profile data, canonical URL, and JSON-LD."""
    # Detect scheme from proxy headers (for production behind reverse proxy)
    scheme = "https" if req.headers.get("x-forwarded-proto") == "https" else "http"
    host = req.headers.get("host") or "127.0.0.1:8000"
    site_url = f"{scheme}://{host}/"
    canonical_url = site_url
    json_ld = build_jsonld(PROFILE, site_url)
    return render_template("index.html", profile=PROFILE, canonical_url=canonical_url, json_ld=json_ld)


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
# Error handlers
# ---------------------------------------------------------------------------
# IMPORTANT: Must pass `profile` to error.html because it extends base.html
# which references profile.name, profile.tagline, profile.avatarUrl, etc.

@app.exception(404)
async def not_found(req, exc):
    """Handle 404 errors - render custom error page."""
    return render_template("error.html", status=404, message="Page not found", profile=PROFILE), 404


@app.exception(500)
async def server_error(req, exc):
    """Handle 500 errors - render custom error page."""
    return render_template("error.html", status=500, message="Internal server error", profile=PROFILE), 500


# ---------------------------------------------------------------------------
# Direct execution (fallback if not using fenrir CLI)
# ---------------------------------------------------------------------------
if __name__ == "__main__":  # pragma: no cover
    app.run()
