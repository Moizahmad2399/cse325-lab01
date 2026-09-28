import subprocess
from datetime import datetime

import pytest


# =============================================================================
# ACTIVITY 1 - Build the smallest working application
# =============================================================================

class Ticket:
    def __init__(self, ticket_id, title):
        self.ticket_id = ticket_id
        self.title = title
        self.status = "OPEN"

    def close(self):
        self.status = "CLOSED"


# =============================================================================
# ACTIVITY 2 - Split responsibilities into modules
# =============================================================================

# ticket.py
class Ticket:
    def __init__(self, ticket_id, title):
        self.ticket_id = ticket_id
        self.title = title
        self.status = "OPEN"


# service.py
def create_ticket(ticket_id, title):
    return Ticket(ticket_id, title)


# =============================================================================
# ACTIVITY 3 - Debug and verify
# =============================================================================

def calculate_priority(hours_waiting):
    if hours_waiting > 24:
        return "HIGH"
    return "NORMAL"


# =============================================================================
# ACTIVITY 4 - Help-desk ticket mini system
# =============================================================================

# ticket.py
PRIORITIES = ("LOW", "MEDIUM", "HIGH")

ALLOWED_MOVES = {
    "OPEN": ["IN_PROGRESS"],
    "IN_PROGRESS": ["CLOSED"],
    "CLOSED": [],
}


class InvalidTransitionError(Exception):
    pass


class HelpDeskTicket:
    def __init__(self, ticket_id, title, priority="MEDIUM"):
        title = title.strip()
        priority = priority.upper()
        if not title:
            raise ValueError("Title cannot be empty")
        if priority not in PRIORITIES:
            raise ValueError("Priority must be one of " + ", ".join(PRIORITIES))
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "OPEN"

    def move_to(self, new_status):
        if new_status not in ALLOWED_MOVES[self.status]:
            raise InvalidTransitionError(
                f"Ticket {self.ticket_id} cannot go from {self.status} to {new_status}"
            )
        self.status = new_status


# service.py
class TicketService:
    def __init__(self):
        self._tickets = {}

    def create(self, ticket_id, title, priority="MEDIUM"):
        if ticket_id in self._tickets:
            raise ValueError(f"Ticket {ticket_id} already exists")
        ticket = HelpDeskTicket(ticket_id, title, priority)
        self._tickets[ticket_id] = ticket
        return ticket

    def get(self, ticket_id):
        if ticket_id not in self._tickets:
            raise KeyError(f"Ticket {ticket_id} not found")
        return self._tickets[ticket_id]

    def change_status(self, ticket_id, new_status):
        ticket = self.get(ticket_id)
        ticket.move_to(new_status)
        return ticket

    def all_tickets(self):
        return list(self._tickets.values())


# display.py
def ticket_summary(ticket):
    return f"#{ticket.ticket_id} | {ticket.title} | {ticket.priority} | {ticket.status}"


def print_all(tickets):
    if not tickets:
        print("No tickets yet")
        return
    for ticket in tickets:
        print(ticket_summary(ticket))


# tests
def test_help_desk_system():
    service = TicketService()

    ticket = service.create(1, "Printer jammed", "low")
    assert ticket.status == "OPEN"
    assert ticket.priority == "LOW"

    service.change_status(1, "IN_PROGRESS")
    assert service.change_status(1, "CLOSED").status == "CLOSED"

    service.create(2, "Portal down", "high")
    with pytest.raises(InvalidTransitionError):
        service.change_status(2, "CLOSED")
    assert service.get(2).status == "OPEN"

    with pytest.raises(InvalidTransitionError):
        service.change_status(1, "OPEN")
    with pytest.raises(InvalidTransitionError):
        service.change_status(2, "DONE")
    with pytest.raises(InvalidTransitionError):
        service.change_status(1, None)

    with pytest.raises(ValueError):
        HelpDeskTicket(3, "   ", "low")
    with pytest.raises(ValueError):
        HelpDeskTicket(3, "Something", "urgent")
    with pytest.raises(ValueError):
        service.create(2, "Duplicate id", "low")
    with pytest.raises(KeyError):
        service.get(999)

    assert calculate_priority(24) == "NORMAL"
    assert calculate_priority(25) == "HIGH"
    assert ticket_summary(HelpDeskTicket(10, "VPN issue", "high")) == "#10 | VPN issue | HIGH | OPEN"


# =============================================================================
# GRADED TASK 1 - Ticket class with created_at and assigned_to
# =============================================================================

class TrackedTicket:
    def __init__(self, ticket_id, title, assigned_to=None):
        self.ticket_id = ticket_id
        self.title = title
        self.status = "OPEN"
        self.created_at = datetime.now()
        self.assigned_to = assigned_to

    def assign(self, person):
        self.assigned_to = person

    def __str__(self):
        owner = self.assigned_to or "unassigned"
        created = self.created_at.strftime("%Y-%m-%d %H:%M")
        return f"#{self.ticket_id} {self.title} [{self.status}] created {created}, {owner}"


# =============================================================================
# GRADED TASK 2 - Valid status transitions, reject invalid ones
# =============================================================================

WORKFLOW_MOVES = {
    "OPEN": ["IN_PROGRESS"],
    "IN_PROGRESS": ["CLOSED"],
    "CLOSED": [],
}


class WorkflowTicket:
    def __init__(self, ticket_id, title):
        self.ticket_id = ticket_id
        self.title = title
        self.status = "OPEN"

    def move_to(self, new_status):
        if new_status not in WORKFLOW_MOVES[self.status]:
            raise InvalidTransitionError(f"{self.status} -> {new_status} is not allowed")
        self.status = new_status


# =============================================================================
# GRADED TASK 3 - Search function that finds tickets by priority
# =============================================================================

class PriorityTicket:
    def __init__(self, ticket_id, title, priority):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority.upper()


def find_by_priority(tickets, priority):
    wanted = priority.upper()
    return [ticket for ticket in tickets if ticket.priority == wanted]


# =============================================================================
# GRADED TASK 4 - README with setup/run instructions
# =============================================================================

README_TEXT = r"""# Help-desk Ticket System

Small Python program for handling student support tickets. Each ticket has a title, priority and status, and moves from OPEN to IN_PROGRESS to CLOSED.

## Requirements

- Python 3.10 or newer
- Git
- pytest (only needed to run the tests)

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest
```

## Run

```powershell
python main.py
```

## Test

```powershell
pytest
```
"""


# =============================================================================
# GRADED TASK 5 - Git history with at least five meaningful commits
# =============================================================================

def commit_count(repo_path="."):
    result = subprocess.run(
        ["git", "log", "--oneline"],
        capture_output=True,
        text=True,
        cwd=repo_path,
    )
    return len(result.stdout.strip().splitlines())


def has_enough_commits(repo_path=".", minimum=5):
    return commit_count(repo_path) >= minimum
