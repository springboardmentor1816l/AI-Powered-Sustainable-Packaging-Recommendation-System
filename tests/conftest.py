import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
