# AGENTS.md

## Web framework
- fenrir-framework (sudah di-install dengan pip)
- pelajari framework secara menyeluruh dan mendalam (~/Documents/fenrir)

## Bahasa
- selalu pakai bahasa indonesia

## Project: uta-home
- Portfolio website dengan Fenrir Framework
- UI 100% identik dengan ~/Documents/Homepage (Nuxt 4 + Tailwind CSS)
- Performance-first: GZip middleware, CDN assets, minimal JS
- Data hardcoded di app.py (tanpa database)
- Deployed to Vercel with GitHub Actions CI/CD

## Perintah
- Jalankan: `fenrir run app:app --host 0.0.0.0 --port 8000`
- Dev mode: `fenrir run app:app --dev`
- Lihat routes: `fenrir routes app:app`
- Jalankan tests: `pytest tests/ -v --cov=. --cov-report=term-missing`

## Struktur
- `app.py` - Entry point Fenrir + data profile + routes
- `api/index.py` - Vercel ASGI entrypoint
- `templates/` - Jinja2 templates (base.html, index.html, error.html)
- `static/` - CSS, JS, assets (local development)
- `public/static/` - CSS, JS, assets (Vercel deployment)
- `tests/` - 116 tests, 100% coverage

## Performance
- GZip middleware aktif (local/production only)
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
- Vercel: automatic deployment from main branch
- GitHub Actions: test on Python 3.10/3.11/3.12, coverage report
- Environment variables: none required (all data hardcoded)
