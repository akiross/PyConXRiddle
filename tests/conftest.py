import os
import pytest
import uuid

from riddle import create_app, database


@pytest.fixture
def test_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['RIDDLE_CONFIG'] = os.path.join(current_dir, '../dev.cfg')
    app = create_app()
    app.config['SQLITE_PATH'] = f'{uuid.uuid4().hex}.db'
    with app.app_context():
        database.init()
    return app


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()
