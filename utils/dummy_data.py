"""
Dummy Banking Data — Mock account data and helper utilities
"""
import random
import string
from datetime import datetime

ACCOUNT_DATA = {
    "name":          "Ahmed Al Mansouri",
    "masked_number": "**** **** **** 4821",
    "last4":         "4821",
    "iban":          "AE07 0331 2345 6789 0123 456",
    "balance":       "AED 24,750.00",
    "balance_float": 24750.00,
    "currency":      "AED",
    "bank":          "Dubai Bank",
    "branch":        "Dubai Main Branch",
    "account_type":  "Current Account",
    "status":        "Active",
}

RECENT_TRANSACTIONS = [
    {"date": "2025-04-20", "desc": "Salary Credit",       "amount": "+AED 8,500.00", "type": "credit"},
    {"date": "2025-04-18", "desc": "DEWA Bill Payment",   "amount": "-AED 320.00",   "type": "debit"},
    {"date": "2025-04-15", "desc": "Supermarket Purchase","amount": "-AED 215.75",   "type": "debit"},
    {"date": "2025-04-10", "desc": "Transfer Received",   "amount": "+AED 1,200.00", "type": "credit"},
    {"date": "2025-04-05", "desc": "ATM Withdrawal",      "amount": "-AED 500.00",   "type": "debit"},
]


def generate_txn_id(prefix: str = "DB") -> str:
    """Generate a random transaction/reference ID."""
    ts   = datetime.now().strftime("%Y%m%d")
    rand = "".join(random.choices(string.digits, k=6))
    return f"{prefix}{ts}{rand}"


def get_dummy_balance_text() -> str:
    """Return a natural-language balance string."""
    return (
        f"Your current account balance is {ACCOUNT_DATA['balance']} "
        f"in your {ACCOUNT_DATA['account_type']} ending in {ACCOUNT_DATA['last4']}."
    )
