from tests.account.fixtures import (
    existing_currency,
    existing_account,
    existing_account_passive,
    existing_account_2,
    existing_account_passive_2,
    active_account_for_user1,
    passive_account_for_user2
)
from tests.funds.fixtures import exs_hundred_rub_passive_to_active
from tests.test_engine import setup_db, db_session, test_client
from tests.user.fixtures import (
    existing_user,
    existing_user2,
    existing_client,
    existing_client_login,
    test_jwt,
    auth_headers,
    existing_client2,
    test_jwt_user2,
    auth_headers_user2,
)
