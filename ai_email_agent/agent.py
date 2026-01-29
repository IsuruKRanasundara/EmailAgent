from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_email(prompt: str):
    """Generate an email body with Claude."""
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=400,
        system="You are a professional email assistant. Keep responses concise and polite.",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.content[0].text if response.content else ""

    return {
        "subject": "AI Generated Email",
        "body": content,
    }
