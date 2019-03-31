import os
from pathlib import Path

import pytest

from riddle import create_app


@pytest.fixture
def test_app():
    os.environ['RIDDLE_CONFIG'] = str(Path(__file__).parent / 'testing.cfg')
    return create_app()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()
