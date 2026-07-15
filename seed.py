"""
One-time MongoDB seeder for project data.
Reads project data from PROFILE in app.py and inserts/upserts into MongoDB.

Usage:
    python seed.py
"""

import os
import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

PROJECTS = [
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
]


async def seed():
    uri = os.environ.get("MONGODB_URI")
    if not uri:
        print("ERROR: MONGODB_URI tidak ditemukan di environment")
        return

    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
    try:
        await client.admin.command("ping")
        print("Terhubung ke MongoDB")
    except Exception as e:
        print(f"Gagal konek: {e}")
        return

    db = client.get_database("uta-home")
    now = datetime.now(timezone.utc)

    for i, p in enumerate(PROJECTS):
        desc = p["description"]
        doc = {
            "title": p["title"],
            "description": desc,
            "description_raw": desc,
            "badges": p.get("badges", []),
            "github": p.get("github", ""),
            "demo": p.get("demo", ""),
            "order": i,
            "created_at": now,
            "updated_at": now,
        }

        existing = await db.projects.find_one({"title": p["title"]})
        if existing:
            await db.projects.update_one({"_id": existing["_id"]}, {"$set": doc})
            print(f"  UPDATE: {p['title']}")
        else:
            await db.projects.insert_one(doc)
            print(f"  INSERT: {p['title']}")

    total = await db.projects.count_documents({})
    print(f"\nSelesai. Total project di database: {total}")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
