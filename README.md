# AI Email Agent

An intelligent email agent that uses AI (OpenAI or Gemini) to generate and send professional emails.

## Features

- 🤖 AI-powered email generation using OpenAI or Google Gemini
- 📧 SMTP email sending (Gmail compatible)
- 🎨 Customizable email tone (professional, casual, formal, etc.)
- 📝 System prompt customization
- 🔧 Environment-based configuration
- 📊 Comprehensive logging

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-email-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Configuration

Edit the `.env` file with your settings:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# AI Service Configuration
AI_PROVIDER=openai  # or 'gemini'
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
AI_MODEL=gpt-4

# Agent Configuration
MAX_RETRIES=3
LOG_LEVEL=INFO
```

### Gmail Setup

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password in `EMAIL_PASSWORD`

## Usage

### Basic Usage

```python
from app.agent.email_agent import EmailAgent

agent = EmailAgent()

# Generate and send an email
agent.generate_and_send(
    recipient="recipient@example.com",
    subject="Meeting Follow-up",
    context="Discussing project timeline",
    tone="professional"
)
```

### Using the Runner

```bash
python run.py
```

## Project Structure

```
ai-email-agent/
├── app/
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration management
│   ├── agent/
│   │   └── email_agent.py   # Main agent logic
│   ├── services/
│   │   ├── email_service.py # SMTP/Gmail sending
│   │   └── ai_service.py    # OpenAI/Gemini integration
│   ├── utils/
│   │   └── logger.py        # Logging utility
│   └── templates/
│       └── system_prompt.txt # AI behavior prompt
├── .env                     # Environment variables
├── requirements.txt
└── README.md
```

## Development

### Running Tests

```bash
# Add your test commands here
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
