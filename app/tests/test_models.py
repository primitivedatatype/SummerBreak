import pytest

from models import TransactionType, Transaction


def test_invalid_transaction_type_format():
    with pytest.raises(ValueError):
        TransactionType(" Income")


def test_invalid_transaction_income_negative():
    with pytest.raises(ValueError):
        Transaction(
            date="2000-01-01",
            xaction_type="Income",
            amount=-1.00,
            memo="Test Negative Income Invalid",
        )


def test_invalid_transaction_income_zero():
    with pytest.raises(ValueError):
        Transaction(
            date="2000-01-01",
            xaction_type="Income",
            amount=0.00,
            memo="Test Zero Income Invalid",
        )


def test_invalid_transaction_xaction_type_format():
    with pytest.raises(ValueError):
        Transaction(
            date="2000-01-01",
            xaction_type=" Income",
            amount=0.00,
            memo="Test Zero Income Invalid",
        )


def test_invalid_transaction_date_format():
    with pytest.raises(ValueError):
        Transaction(
            date="01-01-2000",
            xaction_type="Income",
            amount=0.00,
            memo="Test Zero Income Invalid",
        )


def test_invalid_transaction_amount_format():
    with pytest.raises(ValueError):
        Transaction(
            date="2000-01-01",
            xaction_type="Income",
            amount="0.00",
            memo="Test amount is not a float",
        )
