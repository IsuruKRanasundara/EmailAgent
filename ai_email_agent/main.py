from agent import generate_email
from email_service import send_email

if __name__ == "__main__":
    prompt = "Write a polite follow-up email to a client about a pending invoice."
    recipient = "isururanasundara2@gmail.com"

    email = generate_email(prompt)

    send_email(
        to_email=recipient,
        subject=email["subject"],
        body=email["body"]
    )

    print("✅ Email sent successfully!")
