"""SupportIQ — Intake Service (thin starter stub).

Owns raw ticket data and submission. Deliberately minimal: Exercise A4 plans out
its real structure and API, and later exercises flesh it out. Exercise B4 must
evolve the Classification Service *without changing this file*.
"""

from __future__ import annotations

import json
import os
from typing import Optional


def load_tickets(path: Optional[str] = None) -> list[dict]:
    """Load raw tickets. Intake owns this data; other services receive it via contract."""
    if path is None:
        here = os.path.dirname(__file__)
        path = os.path.abspath(os.path.join(here, "..", "..", "data", "sample_tickets.json"))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_ticket(ticket_id: str) -> Optional[dict]:
    for ticket in load_tickets():
        if ticket.get("id") == ticket_id:
            return ticket
    return None


if __name__ == "__main__":
    tickets = load_tickets()
    print(f"Intake holds {len(tickets)} tickets: {', '.join(t['id'] for t in tickets)}")
