import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

@pytest.fixture(scope="session")
def app():
    from main import app
    return app

