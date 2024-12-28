from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from ..main import app
from sql.engine import get_session
import pytest

from sql.models import Client
    
test_data ={
    "name": "lololoshka",
    "surname": "test2name",
    "birthday": "2024-09-16",
    "sex": "male",
    "document": "passport",
    "docRequisites": "12345",
    "docIssuedBy": "1234",
    "telephone": "+12345",
    "patronymic": "666",
    "serviceEndDate": None
    }

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

@pytest.fixture
def existing_client(db_session: Session):
    data = test_data.copy()
    data['telephone'] = '12345000'
    data['docRequisites'] = '12345000'
    
    new_client = Client(**data
    )
    
    db_session.add(new_client)
    db_session.commit()

    return new_client
        

def test_create_client_success(test_client):
    data = test_data.copy()
    response = test_client.post(
        '/addclient',
        json=data
    )
    assert response.status_code == 200 
    
def test_telephone_exists(existing_client: Client, test_client: TestClient):
    data = test_data.copy()
    data['telephone'] = existing_client.telephone
    response = test_client.post('/addclient',json=data.copy())
    assert response.status_code == 400
    assert response.json()['detail'] == 'telephone exists'

def test_docrecs_exists(existing_client: Client, test_client: TestClient):
    data = test_data.copy()
    data['docRequisites'] = existing_client.docRequisites
    response = test_client.post('/addclient',json=data.copy())
    assert response.status_code == 400
    assert response.json()['detail'] == 'docRequisites exists'
    




