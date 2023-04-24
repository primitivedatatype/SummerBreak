import pytest
from unittest.mock import patch
from pydantic import ValidationError
from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app

client = TestClient(app)


@pytest.fixture
def mock_account():
    with patch("accounting.Account") as MockAccount:
        mock_account = MockAccount.return_value
        mock_account.submit_transaction.return_value = "mock_result"
        mock_account.get_account_summary.return_value = "mock_summary"
        return mock_account


def test_submit_transactions_valid(mock_account):
    with open("./tests/test_main/data.csv", "rb") as f:
        response = client.post("/transactions", files={"data": ("data.csv", f)})
        assert response.status_code == HTTPStatus.OK


def test_submit_transactions_invalid(mock_account):
    with pytest.raises(ValidationError):
        with open("./tests/test_main/invalid_data.csv", "rb") as f:
            response = client.post(
                "/transactions", files={"data": ("invalid_data.csv", f)}
            )
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
