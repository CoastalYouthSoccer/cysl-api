import pytest
#from asyncio import get_event_loop

from starlette.testclient import TestClient
from os.path import (join, abspath, dirname)
import json
from sqlalchemy import insert, MetaData

from app.models import (Season, Misconduct)
#from app.database import init_db, get_session
from main import app

seed_info = {
    "season": Season, "misconduct": Misconduct
}

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client

def load_database(db_session, file_name, data_model):
    with open(file_name) as f_in:
        data = json.load(f_in)
        db_session.execute(insert(data_model), data)

#@pytest.fixture(scope='class', autouse=True)
#async def init_database(request):
#    """Initializes the database """
#    db = get_session()
#    await init_db()
#
#    base_dir = join(abspath(dirname(__file__)))
#
#    for file_name, model_name in seed_info.items():
#        temp_name = join(base_dir, 'seed', f"{file_name}.json")
#        load_database(db, temp_name, model_name)
#
#    request.cls.db = db
#    yield
#    db.close()


#@pytest.fixture(scope='session')
#def event_loop():
#    """Override the default event loop for pytest-asyncio."""
#    loop = get_event_loop()
#    yield loop
#    loop.close()
