"""
Vercel Serverless Function Entry Point
========================================
Imports the Fenrir application and exposes it as an ASGI-compatible handler.
Vercel Python runtime automatically discovers and calls this module when
receiving HTTP requests on the deployed domain (uta.eksashop.web.id).

File location: /api/index.py (Vercel convention for Python serverless functions)
"""

import sys
import os

# ---------------------------------------------------------------------------
# Path setup: ensure the project root is importable
# Vercel runs from /var/task, so we need to add the parent directory.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Fenrir ASGI application instance from the main module
from app import app

# Vercel looks for an ASGI application named 'app' at module level.
# Fenrir is fully ASGI-compatible, so no adapter/wrapper is needed.
