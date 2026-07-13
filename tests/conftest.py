import pytest
import sys
import os

# Add project root to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, PROFILE, build_jsonld


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
