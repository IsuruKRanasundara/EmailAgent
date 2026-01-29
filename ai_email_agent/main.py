"""Entry point for the AI email agent application."""
from agent import generate_email
from email_service import send_email


def main() -> None:
    """Placeholder CLI entrypoint."""
    # TODO: Replace with real prompt/input handling.
    prompt = "Replace this with user input"
    email_body = generate_email(prompt)

    # TODO: Replace with real recipient and subject values.
    recipient = "recipient@example.com"
    subject = "Subject placeholder"
    send_email(recipient, subject, email_body)


if __name__ == "__main__":
    main()
