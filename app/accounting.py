from models import TransactionType, Transaction
from typing import Dict

class Account:
    def __init__(self) -> None:
        self.revenue = 0
        self.expense = 0

    def submit_transaction(self, xaction: Transaction) -> None:
        if xaction.xaction_type == TransactionType.income:
            self.revenue += xaction.amount
        elif xaction.xaction_type == TransactionType.expense:
            self.expense += xaction.amount

    def get_account_summary(self) -> Dict[str, float]:
        return {
            "gross-revenue": self.revenue,
            "expenses": self.expense,
            "net-revenue": self.revenue - self.expense,
        }
