# IshikawaUta Portfolio

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Fenrir-Framework-9b59b6.svg)](https://pypi.org/project/fenrir-framework/)
[![Tests](https://img.shields.io/badge/Tests-116%20Passed-brightgreen.svg)](https://github.com/IshikawaUta/uta-home/actions)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](https://github.com/IshikawaUta/uta-home/actions)
[![CI](https://github.com/IshikawaUta/uta-home/actions/workflows/ci.yml/badge.svg)](https://github.com/IshikawaUta/uta-home/actions/workflows/ci.yml)
[![Deployment](https://img.shields.io/badge/Deployed-Vercel-black.svg)](https://vercel.app)
[![Performance](https://img.shields.io/badge/Performance-High--Speed%20ASGI-orange.svg)]()

Portfolio website built with [Fenrir Framework](https://github.com/IshikawaUta/fenrir), featuring performance-first architecture with no database dependency.

**Live Demo:** [https://uta.eksashop.web.id](https://uta.eksashop.web.id)

## Features

- 100% UI match with original Nuxt 4 + Tailwind CSS design
- Dark/Light theme with View Transitions API animation
- Orbiting tech stack icons with SVG circles
- SEO optimized: JSON-LD, dynamic sitemap.xml, robots.txt, canonical URLs
- Performance-first: GZip compression, CDN assets, minimal JS
- No database - all data hardcoded in Python
- Deployed on Vercel with automatic CI/CD

## Tech Stack

- **Framework:** Fenrir Framework (Python ASGI)
- **Server:** Asteri Server (ASGI)
- **Styling:** Tailwind CSS (CDN)
- **Fonts:** Geist Sans & Mono (Google Fonts)
- **Deployment:** Vercel
- **CI/CD:** GitHub Actions

## Project Structure

```
uta-home/
├── api/
│   └── index.py           # Vercel entrypoint
├── public/
│   └── static/
│       ├── css/style.css   # CSS variables, view transitions
│       └── js/
│           ├── theme-toggle.js
│           └── tech-circles.js
├── static/
│   ├── css/style.css       # Local development CSS
│   └── js/
│       ├── theme-toggle.js
│       └── tech-circles.js
├── templates/
│   ├── base.html           # Base layout
│   ├── index.html          # Main page
│   └── error.html          # 404/500 error page
├── tests/
│   ├── test_app.py         # 116 tests, 100% coverage
│   └── conftest.py         # Pytest fixtures
├── app.py                  # Application entry point
├── vercel.json             # Vercel configuration
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── pyproject.toml          # Project configuration
```

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/IshikawaUta/uta-home.git
cd uta-home

# Install dependencies
pip install -r requirements.txt

# Run development server
fenrir run app:app --dev
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Production

```bash
# Run with multiple workers
fenrir run app:app --host 0.0.0.0 --port 8000 --workers 2

# View available routes
fenrir routes app:app
```

## Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ -v --cov=. --cov-report=html
```

Current coverage: **100%** (116 tests)

## Deployment

### Vercel

1. Push to GitHub
2. Import repository in Vercel dashboard
3. Deploy automatically

### Environment Variables

No environment variables required. All data is hardcoded in `app.py`.

## Customization

Edit the `PROFILE` dictionary in `app.py` to customize:

- Name, tagline, and avatar
- About text paragraphs
- Tech stack icons
- Social links
- Achievement cards

## Performance

- GZip compression enabled (local/production)
- Tailwind CSS via CDN (no build step)
- Geist fonts via Google Fonts CDN
- JavaScript deferred loading
- Image lazy loading
- CSS View Transitions API for theme toggle
- Static assets cached with immutable headers

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**Eka Saputra** - [@IshikawaUta](https://github.com/IshikawaUta)

- GitHub: [github.com/IshikawaUta](https://github.com/IshikawaUta)
- Blog: [ishikawauta.github.io/my-blogs](https://ishikawauta.github.io/my-blogs)
- Email: komikers09@gmail.com
