import datetime
from enum import Enum, IntEnum
from pydantic import BaseModel, validator, root_validator
from pydantic.main import ModelMetaclass
from typing import Any, Dict


class TransactionType(str, Enum):
    income = "Income"
    expense = "Expense"


class Transaction(BaseModel):
    date: datetime.date
    xaction_type: str
    amount: float  # TODO: change this to use decimal
    memo: str

    class Config:
        anystr_strip_whitespace = True

    @root_validator()
    def validate_income(cls: ModelMetaclass, values: Dict[str, Any]):
        """
        @param: cls
        instance of ModelMetaclass

        Income amounts should never be negative or 0.
        (Refunds can be represented as negative values on expenses), so those are still valid).
        """
        if values.get("xaction_type") == TransactionType.income:
            if values.get("amount") <= 0:
                raise ValueError(
                    f"Income entry with value <= 0 is invalid: {values.get('amount')}"
                )
        return values
