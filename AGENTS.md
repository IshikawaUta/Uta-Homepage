# AGENTS.md

## Web framework
- fenrir-framework (sudah di-install dengan pip)
- pelajari framework secara menyeluruh dan mendalam (~/Documents/fenrir)

## Bahasa
- selalu pakai bahasa indonesia

## Project: uta-home
- Portfolio website dengan Fenrir Framework
- UI 100% identik dengan ~/Documents/Homepage (Nuxt 4 + Tailwind CSS)
- Performance-first: GZip middleware, CDN assets, minimal JS, 60s cache
- **MongoDB Atlas** via async **Motor** driver (fallback ke hardcoded data)
- Admin CMS: login, CRUD projects (CSRF protected, rate limited, session TTL)
- Security: XSS sanitized (bleach), CSRF tokens, timing-safe compare, bcrypt
- Deployed to Vercel + Docker with Cloudflare Tunnel

## Perintah
- Jalankan: `fenrir run app:app --host 0.0.0.0 --port 8000`
- Dev mode: `fenrir run app:app --dev`
- Lihat routes: `fenrir routes app:app`
- Jalankan tests: `pytest tests/ -v --cov=. --cov-report=term-missing`
- Docker build: `docker compose up -d --build`
- Docker logs: `docker compose logs -f`

## Struktur
- `app.py` - Entry point Fenrir + data profile + routes
- `api/index.py` - Vercel ASGI entrypoint
- `templates/` - Jinja2 templates (base.html, index.html, error.html)
- `templates/admin/` - Admin templates (dashboard, login, project form)
- `static/` - CSS, JS, assets (local development)
- `public/static/` - CSS, JS, assets (Vercel deployment)
- `tests/` - 194 tests, 100% coverage
- `seed.py` - One-time MongoDB seeder untuk project data
- `Dockerfile` - Docker image (Python 3.12-slim + uvicorn)
- `docker-compose.yml` - Web + Cloudflare Tunnel services
- `.dockerignore` - Exclude .env, tests, dev files
- `.env` - Cloudflare Tunnel token + MONGODB_URI (tidak di-commit)
- `.env.example` - Template environment variables

## Performance
- GZip middleware aktif (local/production, skip di Docker)
- Tailwind CSS via CDN
- Geist fonts via Google Fonts CDN
- JS deferred loading
- Image lazy loading
- CSS View Transitions API untuk theme toggle
- Static assets cached with immutable headers (Vercel)

## SEO
- JSON-LD structured data (schema.org ProfilePage)
- Dynamic sitemap.xml
- Dynamic robots.txt
- Canonical URLs with dynamic scheme/host
- Open Graph meta tags (og:title, og:description, og:image, og:url, og:logo)
- Twitter Card meta tags (twitter:title, twitter:description, twitter:image)
- Comprehensive keywords meta tag

## Deployment
### Vercel
- Automatic deployment from main branch
- GitHub Actions: test on Python 3.10/3.11/3.12, coverage report
- URL: https://uta.eksashop.web.id

### Docker + Cloudflare Tunnel
- Uvicorn server (2 workers) di container `ishikawauta-portfolio`
- Cloudflare Tunnel di container `cloudflare-tunnel` (HTTP/2)
- Port: 8888
- URL: https://folio.eksashop.web.id
- Cloudflare Zero Trust: Bot Challenge aktif
- `.env` berisi `CLOUDFLARE_TUNNEL_TOKEN` (dibaca docker-compose)
- Token di-pass sebagai `TUNNEL_TOKEN` env var (bukan di command args)
- `.dockerignore` mengecualikan `.env` supaya tidak bocor ke image layers

## Environment Variables
- `VERCEL` - Auto-set oleh Vercel (skip GZip + static mount)
- `DOCKER` - Auto-set di Dockerfile (skip GZip, tetap mount static)
- `CLOUDFLARE_TUNNEL_TOKEN` - Hanya di `.env`, dibaca docker-compose
