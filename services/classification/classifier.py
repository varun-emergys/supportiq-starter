"""SupportIQ — Classification & Triage Service (rule-based starter).

This is the starter implementation: deterministic, keyword-driven classification.
Exercise B4 replaces the internals of `classify()` with a Claude-powered version
*without changing this module's public interface* — so the Intake Service and the
A5 tests keep working untouched.

Public interface (the contract B4 must preserve):
    classify(ticket: dict) -> dict
        input  ticket: {"id": str, "subject": str, "body": str, ...}
        output result: {"id", "category", "priority", "sentiment"}

Categories: network, hardware, software, access, email, other
Priorities: critical, high, medium, low
Sentiment:  frustrated, neutral, urgent
"""

from __future__ import annotations

import json
import os
from typing import Iterable


CATEGORIES = ("network", "hardware", "software", "access", "email", "other")
PRIORITIES = ("critical", "high", "medium", "low")
SENTIMENTS = ("frustrated", "neutral", "urgent")

# Keyword tables. Order of CATEGORIES above is also the tie-break order.
_CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "network": ("vpn", "wifi", "wi-fi", "wireless", "network", "connect", "connection",
                "dns", "internet", "disconnect"),
    "hardware": ("laptop", "charger", "charging", "dock", "docking", "monitor", "display",
                 "keyboard", "mouse", "printer", "battery", "screen"),
    "software": ("install", "app", "application", "crash", "update", "license", "licensing",
                 "software", "photoshop", "version"),
    "access": ("password", "sso", "login", "log in", "locked", "lockout", "account",
                "permission", "access", "credentials"),
    "email": ("email", "outlook", "mailbox", "calendar", "invite", "spam", "phishing",
              "distribution list"),
}

# Words that push priority up. Checked against subject + body, lowercased.
_CRITICAL_SIGNALS = ("everyone", "whole office", "all users", "production", "outage",
                     "customers affected", "compromised", "suspicious login",
                     "security", "breach", "down — ", "are down", "is down")
_HIGH_SIGNALS = ("locked out", "completely locked", "can't", "cannot", "blocked",
                 "unable", "stopped working", "won't")
_LOW_SIGNALS = ("no rush", "not urgent", "low priority", "sometime this week",
                "nice to have", "cosmetic", "still usable", "manageable")

_FRUSTRATED_SIGNALS = ("again", "still", "annoying", "frustrat", "missed", "worried",
                       "keeps", "every 10 minutes")
_URGENT_SIGNALS = ("now", "asap", "urgent", "immediately", "in an hour", "right now")


def _text(ticket: dict) -> str:
    return f"{ticket.get('subject', '')} {ticket.get('body', '')}".lower()


def _category(text: str) -> str:
    best, best_hits = "other", 0
    for cat in CATEGORIES:
        if cat == "other":
            continue
        hits = sum(1 for kw in _CATEGORY_KEYWORDS[cat] if kw in text)
        # The category's own name appearing in the text is a strong signal.
        if cat in text:
            hits += 1
        if hits > best_hits:
            best, best_hits = cat, hits
    return best


def _priority(text: str) -> str:
    if any(sig in text for sig in _CRITICAL_SIGNALS):
        return "critical"
    if any(sig in text for sig in _LOW_SIGNALS):
        return "low"
    if any(sig in text for sig in _HIGH_SIGNALS):
        return "high"
    return "medium"


def _sentiment(text: str) -> str:
    if any(sig in text for sig in _URGENT_SIGNALS):
        return "urgent"
    if any(sig in text for sig in _FRUSTRATED_SIGNALS):
        return "frustrated"
    return "neutral"


def classify(ticket: dict) -> dict:
    """Classify a single ticket. Stable public interface — see module docstring."""
    text = _text(ticket)
    return {
        "id": ticket.get("id"),
        "category": _category(text),
        "priority": _priority(text),
        "sentiment": _sentiment(text),
    }


def classify_all(tickets: Iterable[dict]) -> list[dict]:
    return [classify(t) for t in tickets]


def _load_sample_tickets() -> list[dict]:
    here = os.path.dirname(__file__)
    path = os.path.join(here, "..", "..", "data", "sample_tickets.json")
    with open(os.path.abspath(path), encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    tickets = _load_sample_tickets()
    for result in classify_all(tickets):
        print(f"{result['id']:>7}  "
              f"{result['category']:<9}  "
              f"{result['priority']:<8}  "
              f"{result['sentiment']}")


if __name__ == "__main__":
    main()
