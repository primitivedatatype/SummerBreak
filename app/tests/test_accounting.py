import pytest
from accounting import Account
from models import TransactionType, Transaction
import datetime


@pytest.fixture
def mock_date() -> datetime.datetime:
    return datetime.datetime.now()


@pytest.fixture
def mock_transaction(mock_date: datetime.datetime) -> Transaction: 
    mock_transaction = Transaction(
        date=mock_date, xaction_type="Income", amount=40.00, memo="test data"
    )
    return mock_transaction


@pytest.fixture
def shared_account() -> Account:
    account = Account()
    return account


def test_submit_transactions(shared_account: Account, mock_transaction: Transaction) -> None:
    shared_account.submit_transaction(mock_transaction)
    assert shared_account.expense == 0


def test_get_account_summary(shared_account: Account, mock_transaction: Transaction) -> None:
    shared_account.submit_transaction(mock_transaction)
    assert shared_account.get_account_summary() == {
        "gross-revenue": pytest.approx(40),
        "expenses": pytest.approx(0),
        "net-revenue": pytest.approx(40),
    }
