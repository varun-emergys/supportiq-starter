# SupportIQ — AI-Augmented IT Helpdesk (Workshop Starter)

SupportIQ is the running use case for the *Engineering AI-Native Systems with Claude* workshop.
It is an IT helpdesk / ticketing platform, built progressively as a set of independent
microservices. This repository is the **starter skeleton** — Lab Block A begins from here.

> Note: there is intentionally **no root `CLAUDE.md`** in this starter. You create it in
> Exercise A2. Everything the agent needs to write a good one is already here: this README,
> the sample tickets in `data/`, and the rule-based classifier in `services/classification/`.

## Domain at a glance

A user submits a ticket. The system classifies and triages it, tracks its lifecycle, notifies
owners on critical issues, and can surface similar past tickets. The workshop builds five
services; this starter ships two of them in thin form.

### Ticket categories
- `network` — VPN, Wi-Fi, connectivity, DNS
- `hardware` — laptops, peripherals, docking stations, displays
- `software` — application installs, crashes, licensing, updates
- `access` — passwords, SSO, account lockouts, permissions
- `email` — mailbox, calendar, distribution lists, spam
- `other` — anything that does not match the above

### Priority levels
- `critical` — outage or security exposure; many users blocked or business-critical
- `high` — single user fully blocked from core work
- `medium` — degraded but workable; intermittent issues
- `low` — cosmetic, informational, or "nice to have"

### Sentiment
- `frustrated`, `neutral`, `urgent` — coarse signal used for routing emphasis only

## Services (target architecture)

| Service | Owns | Status in starter |
|---|---|---|
| Intake | Raw ticket data, submission | thin stub (`services/intake/`) |
| Classification & Triage | category, priority, sentiment | **working, rule-based** (`services/classification/`) |
| Workflow / Lifecycle | open → in-progress → resolved → closed | built during labs |
| Notification & Escalation | alerts on critical tickets | built during labs (B2) |
| Knowledge Base / Retrieval | similar past tickets & docs | built during labs (B2) |

Services talk through **versioned API contracts**, never shared internals. That boundary is
what the "independent evolution" story (Exercise B4) depends on.

## Coding conventions

- Python 3.11+, standard library only in the starter (no install step to begin).
- One service per folder under `services/`; each owns its own data and exposes a small,
  documented Python interface (later, an HTTP/OpenAPI contract — Exercise B3).
- Functions are typed and small; pure logic is kept separate from I/O so it is testable.
- Tests live in `tests/`, named `test_<thing>.py`, runnable with `pytest`.
- No secrets in code. Configuration comes from environment variables.

## Running things

```bash
# Classify the sample tickets with the rule-based classifier
python -m services.classification.classifier

# Run tests (after Exercise A5 generates them)
pytest
```

## Lab starting points (facilitator reference)

- **A1** runs in a *separate empty folder*, not here.
- **A2** → create the root `CLAUDE.md` via `/init`.
- **A3** → re-classify the VPN ticket inside this repo.
- **A4** → plan Intake + Classification structure (folders already exist, deliberately thin).
- **A5** → generate tests into `tests/`.
- **B4** → replace the rule-based classifier with a Claude-powered one *without touching Intake*,
  then re-run the A5 tests.
