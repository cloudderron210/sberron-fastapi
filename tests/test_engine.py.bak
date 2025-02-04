from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from main import app
from sql.engine import get_session
import pytest

DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

@pytest.fixture(scope='session')
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(setup_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def test_client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_session] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

