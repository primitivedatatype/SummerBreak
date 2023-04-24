from io import BytesIO
import pytest
from unittest.mock import patch, mock_open, MagicMock
from pydantic import ValidationError
from fastapi.testclient import TestClient
from http import HTTPStatus
import main
from main import app, submit_transactions, get_report

client = TestClient(app)


@pytest.fixture
def mock_data():
    mock_data = [
        {
            "date": "2000-01-01",
            "xaction_type": "Income",
            "amount": 12.00,
            "memo": "mock_data",
        }
    ]
    return mock_data


@pytest.fixture
def mock_iterdecode(mocker, mock_data):
    mock_iterdecode = mocker.patch("main.codecs.iterdecode")
    mock_iterdecode.return_value = mock_data
    return mock_iterdecode


@pytest.fixture
def mock_dict_reader(mocker, mock_data):
    iterable_mock = MagicMock(return_value=iter(mock_data))

    reader = MagicMock(return_value=iterable_mock)
    reader.__iter__.return_value = iter(mock_data)

    mock_dict_reader = mocker.patch("main.csv.DictReader")
    mock_dict_reader.return_value = reader

    return mock_dict_reader


@pytest.fixture
def mock_transaction(mocker):
    transaction = MagicMock(return_value="mock transaction")
    transaction.parse_obj.return_value = "mock parse data"
    mock_transaction = mocker.patch("main.Transaction")
    mock_transaction.return_value = transaction
    return mock_transaction


@pytest.fixture
def mock_account(mocker):
    account = MagicMock(return_value="mock account")
    account.submit_transaction.return_value = "mock function"
    mock_account = mocker.patch("main.account")
    mock_account.return_value = account
    return mock_account


@pytest.fixture
def mock_file(mocker):
    mock_file = BytesIO(b"data")  # bytes('data', 'utf-8'))
    return mock_file


@pytest.fixture
def mock_open_func(mocker, mock_file):
    _mock_open = mocker.patch("builtins.open")
    _mock_open.return_value = mock_file
    return _mock_open


def test_submit_transactions_calls(
    mocker, mock_data, mock_iterdecode, mock_dict_reader, mock_transaction, mock_account
):
    with open("./tests/test_main/data.csv", "rb") as f:
        response = client.post("/transactions", files={"data": ("data.csv", f)})
        mock_iterdecode.assert_called_once()
        mock_dict_reader.assert_called_once()
        mock_transaction.parse_obj.assert_called()
        mock_account.submit_transaction.assert_called()

        # f.close.assert_called_once()
        assert response.status_code == HTTPStatus.OK


@patch("accounting.Account.submit_transaction")
def test_submit_transactions_invalid(mock_submit_transaction):
    with pytest.raises(ValidationError):
        with open("./tests/test_main/invalid_data.csv", "rb") as f:
            response = client.post(
                "/transactions", files={"data": ("invalid_data.csv", f)}
            )
            mock_submit_transaction.assert_not_called()
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@patch("accounting.Account.get_account_summary")
def test_get_account_summary(mock_get_account_summary):
    response = client.get("/report")
    assert response.status_code == HTTPStatus.OK
    mock_get_account_summary.assert_called_once()
