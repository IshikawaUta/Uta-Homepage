"""
Pytest configuration and shared fixtures for uta-home tests.

Sets up:
- Project root in sys.path (for importing app.py)
- Test credentials (overriding any .env file)
- Clean global state before each test session
- CSRF disabled (tests use direct form submission)
- Async backend (anyio) for async route testing
"""

import pytest
import sys
import os

# Add project root to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, PROFILE

# ---------------------------------------------------------------------------
# Test environment setup
# ---------------------------------------------------------------------------

# Force test credentials (overrides any .env file)
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "admin123"

# Remove MongoDB URI to avoid accidental connections during tests
os.environ.pop("MONGODB_URI", None)

# Reset global state so each test session starts clean
import app as _app_mod
_app_mod._admin_password_hash = None
_app_mod.mongo_db = None
_app_mod.mongo_client = None
_app_mod._projects_cache = None

# Disable CSRF protection during tests (test client doesn't manage cookies/CSRF tokens)
app.config.setdefault("DISABLE_CSRF", True)


@pytest.fixture
def anyio_backend():
    """Required by pytest.mark.anyio for async route testing."""
    return "asyncio"


@pytest.fixture
def client():
    """Create and return a Fenrir test client for HTTP request simulation."""
    return app.test_client()


@pytest.fixture
def sample_site_url():
    """Return a sample site URL used by build_jsonld() tests."""
    return "http://localhost:8000"
