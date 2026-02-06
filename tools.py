from smolagents import tool
import json
from pathlib import Path


@tool
def classify_email(email_text: str) -> str:
    """
    Classify the email intent.

    Args:
        email_text: Raw email content to categorize.

    Returns:
        Category label: billing, scheduling, marketing, or general.
    """

    text = email_text.lower()

    if "invoice" in text or "payment" in text:
        return "billing"

    if "meeting" in text or "reschedule" in text:
        return "scheduling"

    if "unsubscribe" in text or "offer" in text:
        return "marketing"

    return "general"


@tool
def extract_todos(email_text: str) -> str:
    """
    Extract TODO actions from email.

    Args:
        email_text: Raw email content to scan for action items.

    Returns:
        JSON-encoded list of TODO strings.
    """

    todos = []
    text = email_text.lower()

    if "share" in text and "status" in text:
        todos.append("Share latest project status")

    if "meeting" in text and "move" in text:
        todos.append("Propose new meeting times")

    return json.dumps(todos)


@tool
def save_draft(to: str, subject: str, body: str) -> str:
    """
    Save email draft locally.

    Args:
        to: Recipient address.
        subject: Email subject line.
        body: Email body content.

    Returns:
        Path to the saved draft file.
    """

    folder = Path("outbox")
    folder.mkdir(exist_ok=True)

    file = folder / f"{subject.replace(' ', '_')}.txt"

    file.write_text(
        f"TO: {to}\nSUBJECT: {subject}\n\n{body}",
        encoding="utf-8"
    )

    return f"Draft saved at {file}"
