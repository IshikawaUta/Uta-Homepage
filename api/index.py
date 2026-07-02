"""
Vercel Serverless Entry Point for IshikawaUta Portfolio.
Imports the Fenrir app from app.py and exposes it as ASGI application.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects an ASGI application named 'app'
# Fenrir is ASGI-compatible, so we can use it directly
