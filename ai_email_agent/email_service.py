"""SMTP email sending utilities."""

def send_email(recipient: str, subject: str, body: str) -> None:
    """Send an email via SMTP."""
    # TODO: Implement SMTP delivery using credentials from config.
    print(f"Sending email to {recipient} with subject '{subject}'\n{body}")
