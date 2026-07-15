import pytest
import sys
import os

# Add project root to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, PROFILE, build_jsonld

# Force test credentials (overrides any .env file)
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "admin123"

# Remove MongoDB URI to avoid accidental connections during tests
os.environ.pop("MONGODB_URI", None)

# Reset global state
import app as _app_mod
_app_mod._admin_password_hash = None
_app_mod.mongo_db = None
_app_mod.mongo_client = None
_app_mod._projects_cache = None

# Disable CSRF protection during tests
app.config.setdefault("DISABLE_CSRF", True)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def client():
    """Create a test client for the Fenrir app."""
    return app.test_client()


@pytest.fixture
def sample_site_url():
    """Return a sample site URL for testing."""
    return "http://localhost:8000"
