from fastapi.testclient import TestClient
from sqlmodel import Session
from routers.account import AddAccount
from routers.move_money import MoveMoney
from sql.models import Account, MoveMoneyOrder
from tests.test_engine import setup_db, db_session, test_client
import pytest



account_data = {
    "owner_id": 1,
    "currency_id": "810",
    "balNum": "12345",
    "description": "set",
    "isActive": False
} 
test_data = {
    'strAccDb': '0',
    'strAccCr': '0',
    'amount': 1000.00,
    'execute': True,
    'description': 'test'
}

@pytest.fixture
def base_data():
    test_data = {
        'strAccDb': '0',
        'strAccCr': '0',
        'amount': 1000.00,
        'execute': True,
        'description': 'test'
    }
    return test_data


def new_acc(isActive: bool, numAccount: str, db_session):
    account_data = AddAccount(owner_id=1, balNum='12345', currency_id=840, description='test', isActive=isActive).model_dump()
    account_data['numAccount'] = numAccount
    new_account= Account(**account_data)
    db_session.add(new_account)
    db_session.commit()
    db_session.refresh(new_account)
    return new_account

def test_successfull_transer(test_client: TestClient, db_session: Session, base_data: dict):
    new_account_pas = new_acc(isActive=False, numAccount='23432840744440000001', db_session=db_session)
    new_account_act= new_acc(isActive=True, numAccount='23432840744440000002', db_session=db_session)

    data = base_data.copy()
    data['strAccDb'] = new_account_pas.numAccount
    data['strAccCr'] = new_account_act.numAccount
    
    response = test_client.post('/moveMoney', json=data)

    assert response.status_code == 200
    assert response.json()['result'] 

    response = test_client.post('/balance', json={'idAccount': f'{new_account_act.id}' })

    assert response.status_code == 200
    assert response.json()['available'] == 1000

def test_insufficient(base_data: dict, test_client: TestClient, db_session: Session):
    
    source_account = new_acc(isActive=True, numAccount='23432840744440000003', db_session=db_session)
    target_account = new_acc(isActive=True, numAccount='23432840744440000004', db_session=db_session)
    funding_account = new_acc(isActive=False, numAccount='23432840744440000005', db_session=db_session)

    data = base_data.copy()

    data['strAccDb'] = funding_account.numAccount
    data['strAccCr'] = source_account.numAccount
    data['amount'] = 1000

    test_client.post('/moveMoney', json=data)

    transfer_data = base_data.copy()

    transfer_data['strAccDb'] = source_account.numAccount
    transfer_data['strAccCr'] = target_account.numAccount
    transfer_data['amount'] = 1001

    response = test_client.post('/moveMoney', json=transfer_data)

    assert response.status_code == 400
    assert response.json()['detail'] == 'insufficient amount on accDb' 

    
def test_negative_balance(test_client: TestClient, base_data: dict):
    source_active = new_acc(isActive=True, numAccount='23432840744440000006', db_session=db_session)
    target_passive = new_acc(isActive=False, numAccount='23432840744440000007', db_session=db_session)
    funding_account = new_acc(isActive=False, numAccount='23432840744440000008', db_session=db_session)
    
    data = base_data.copy()

    data['strAccDb'] = funding_account.numAccount
    data['strAccCr'] = source_active.numAccount
    data['amount'] = 1000

    test_client.post('/moveMoney', json=data)

    data['strAccDb'] = source_active.numAccount
    data['strAccCr'] = target_passive.numAccount
    data['amount'] = 1000

    response = test_client.post('/moveMoney', json=data)

    assert response.status_code == 400
    assert response.json()['detail'] == 'balance cannot be lower than 0' 



    
    

    
    
    
    
    
# def test_success(test_client: TestClient, db_session: Session):
#     new_account_pas = new_acc(isActive=False, numAccount='23432840744440000001', db_session=db_session)
#     new_account_act= new_acc(isActive=True, numAccount='23432840744440000002', db_session=db_session)
#
#     data = base_data().copy()
#     data['strAccDb'] = new_account_pas.numAccount
#     data['strAccCr'] = new_account_act.numAccount
#     
#     response = test_client.post('/moveMoney', json=data)
#
#     assert response.status_code == 200
#     assert response.json()['result'] 
#
#     response = test_client.post('/balance', json={'idAccount': f'{new_account_act.id}' })
#
#     assert response.status_code == 200
#     assert response.json()['available'] == 1000
#
#     response = test_client.post('/balance', json={'idAccount': 11 })
#
#     assert response.status_code == 400
#     assert response.json()['detail'] == 'account not found' 
#
#     new_account_pas2 = new_acc(isActive=False, numAccount='23432840744440000003', db_session=db_session)
#     new_account_act2 = new_acc(isActive=True, numAccount='23432840744440000004', db_session=db_session)
#
#     data['strAccDb'] = new_account_act.numAccount
#     data['strAccCr'] = new_account_act2.numAccount
#     data['amount'] = 1001
#     response = test_client.post('/moveMoney', json=data)
#
#     assert response.status_code == 400
#     assert response.json()['detail'] == 'insufficient amount on accDb'
#     
#     data['strAccDb'] = new_account_act.numAccount
#     data['strAccCr'] = new_account_pas2.numAccount
#     data['amount'] = 900
#     response = test_client.post('/moveMoney', json=data)
#     
#     assert response.status_code == 400
#     assert response.json()['detail'] == 'balance cannot be lower than 0'
#
#     
# def test_fail(test_client: TestClient, db_session: Session):
#     new_account_pas = new_acc(isActive=False, numAccount='23432840744440000001', db_session=db_session)
#
#     new_account_act= new_acc(isActive=True, numAccount='23432840744440000002', db_session=db_session)
#
#     # new_order 
#
#     data = test_data.copy()
#     data['strAccDb'] = new_account_act.numAccount
#     data['strAccCr'] = new_account_pas.numAccount
#     
#     response = test_client.post('/moveMoney', json=data)
#
#     assert response.status_code == 400
#     assert response.json()['detail'] == 'insufficient amount on accDb'

    
    


