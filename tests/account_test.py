
import pytest
from sqlmodel import Session, select
from routers.account import AddAccount
from sql.models import Account, Client, Currency
from tests.test_engine import setup_db, db_session, test_client
from tests.client_test import existing_client
import time

from fastapi.testclient import TestClient



test_data = {
    "owner_id": 1,
    "currency_id": 810,
    "balNum": "23433",
    "description": "set",
    "isActive": True 
}

@pytest.fixture
def existing_currencys (db_session: Session):
    data = {
        'id': 810,
        'str_code': 'RUB',
        'name': 'rubles'
    }
    new_currency1 = Currency(**data)
    db_session.add(new_currency1)
    db_session.commit()
    db_session.refresh(new_currency1)
    return new_currency1

def test_succesfull(existing_currencys: Currency, existing_client: Client, test_client: TestClient, db_session: Session):
    data = test_data.copy()
    response = test_client.post('/addaccount', json=data)
    
    assert response.status_code == 200
    new_account = db_session.exec(select(Account).where(Account.numAccount == response.json()['new_account']['numAccount'])).first()
    assert new_account is not None
    assert new_account.id == existing_client.id


    
def test_currency_not_exist(existing_client: Client, test_client: TestClient):
    data = test_data.copy()
    data['currency_id'] = 811
    response = test_client.post('/addaccount', json=data)
    assert response.json()['detail'] == 'no such currency'
    
def test_owner_exists(existing_client: Client, test_client: TestClient):
    data = test_data.copy()
    data['owner_id'] = 11
    response = test_client.post('/addaccount', json=data)
    assert existing_client.id == 1
    assert response.status_code == 400
    assert response.json()['detail'] == 'there are no Client with such id'

def test_balnum(test_client: TestClient):
    data = test_data.copy()
    data['balNum'] = 'abcde'
    response = test_client.post('/addaccount', json=data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'value_error'
    assert response.json()['detail'][0]['msg'] == 'Value error, must contain only digits'
    

    
def test_get_accounts(test_client: TestClient):
    response = test_client.get('getaccounts')
    assert type(response.json()['accs']) == list

def test_performance(db_session: Session, test_client: TestClient):
    for i in range(1,10):
        account_data = AddAccount(owner_id=1, balNum='12345', currency_id=840, description='test', isActive=True)
        data = account_data.model_dump()
        data['numAccount'] = f"{23432840744440000001 + i}"
        new_account = Account(**data)
        db_session.add(new_account)
    db_session.commit()
        
    start_time = time.time()
    response = test_client.get('/getaccounts')
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 1
    
