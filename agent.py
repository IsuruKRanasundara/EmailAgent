import os
from smolagents import CodeAgent, InferenceClientModel
from tools import classify_email, extract_todos, save_draft


def build_email_agent():
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        # Fail fast with a clear message instead of surfacing downstream client errors
        raise ValueError(
            "Missing HUGGINGFACEHUB_API_TOKEN environment variable; set it to your Hugging Face token."
        )

    model = InferenceClientModel(
        model_id="meta-llama/Llama-3.3-70B-Instruct",
        token=token
    )

    agent = CodeAgent(
        tools=[classify_email, extract_todos, save_draft],
        model=model,
        add_base_tools=False
    )

    return agent
