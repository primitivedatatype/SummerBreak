import pytest

from models import TransactionType, Transaction


def test_transaction_type_invalid() -> None:
    with pytest.raises(ValueError):
        TransactionType(" Income")


def test_validate_income_invalid_amount_negative() -> None:
    with pytest.raises(ValueError):
        Transaction(
            date="2000-01-01",
            xaction_type="Income",
            amount=-1.00,
            memo="Test Negative Income Invalid",
        )


def test_validate_transaction_invalid_amount_zero() -> None:
    with pytest.raises(ValueError):
        Transaction(
            date="2000-01-01",
            xaction_type="Income",
            amount=0.00,
            memo="Test Zero Income Invalid",
        )


def test_validate_transaction_valid_xaction_type_format() -> None:
    Transaction(
        date="2000-01-01",
        xaction_type=" Income",
        amount=1.00,
        memo="Test Whitespace Parsing on Xaction Type Resolves",
    )


def test_validate_transaction_invalid_date_format() -> None:
    with pytest.raises(ValueError):
        Transaction(
            date="01-01-2000",
            xaction_type="Income",
            amount=0.00,
            memo="Test Date Format Invalid",
        )


def test_validate_transaction_invalid_amount_format() -> None:
    with pytest.raises(ValueError):
        Transaction(
            date="2000-01-01",
            xaction_type="Income",
            amount="0.00",
            memo="Test amount is not a float",
        )
