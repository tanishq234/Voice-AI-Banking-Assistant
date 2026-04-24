"""
Intent Detection Engine
Basic NLP using regex patterns to detect user intent from text.
"""
import re
from typing import Optional

INTENT_PATTERNS = {
    "greeting": [
        r'\b(hi|hello|hey|howdy|good\s?(morning|afternoon|evening|day)|assalam|salam|namaste)\b',
    ],
    "balance": [
        r'\b(balance|how\s*much|funds|account\s*info|check\s*account|my\s*money|available|credit|debit)\b',
        r'\b(what.s\s*in\s*my\s*account|show\s*balance|account\s*balance)\b',
    ],
    "transfer": [
        r'\b(transfer|send\s*money|wire|pay\s*(someone|to|money)|remit|move\s*money)\b',
        r'\b(i\s*want\s*to\s*(send|pay|transfer))\b',
    ],
    "cheque": [
        r'\b(cheque|check|upload\s*cheque|scan\s*cheque|verify\s*cheque|cheque\s*verification)\b',
        r'\b(upload|scan)\b.*\b(image|photo|picture|document)\b',
    ],
    "kyc": [
        r'\b(kyc|know\s*your\s*customer|identity\s*verify|start\s*kyc|verification|verify\s*me)\b',
        r'\b(complete\s*kyc|kyc\s*process|submit\s*kyc)\b',
    ],
    "confirm": [
        r'^(yes|yeah|yep|confirm|ok|okay|sure|proceed|go\s*ahead|correct|absolutely|affirmative)[\s!.]*$',
    ],
    "deny": [
        r'^(no|nope|cancel|stop|abort|reject|negative|never)[\s!.]*$',
    ],
    "help": [
        r'\b(help|what\s*can\s*you\s*do|features|options|menu|services|commands|guide)\b',
        r'\b(i\s*need\s*help|can\s*you\s*help|assist\s*me)\b',
    ],
}


def detect_intent(text: str) -> str:
    """
    Detect the user's intent from input text.
    Returns one of: greeting, balance, transfer, cheque, kyc, confirm, deny, help, unknown
    """
    text_lower = text.lower().strip()

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return intent

    return "unknown"


def extract_entities(text: str) -> dict:
    """
    Extract named entities like amounts, account numbers from text.
    """
    entities = {}
    amount_match = re.search(
        r'(?:aed|usd|dhs?|dirhams?)?\s*(\d[\d,]*(?:\.\d{1,2})?)\s*(?:aed|usd|dirhams?)?',
        text, re.IGNORECASE
    )
    if amount_match:
        entities["amount"] = amount_match.group(0).strip()

    acct_match = re.search(r'\b(\d[\d\s\-]{7,19}\d)\b', text)
    if acct_match:
        entities["account"] = acct_match.group(0).strip()

    return entities
