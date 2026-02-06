import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import AgentExecutor, create_openai_tools_agent

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if not openai_key or not anthropic_key:
    raise RuntimeError("Set OPENAI_API_KEY and ANTHROPIC_API_KEY in .env or the environment.")

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
llm2 = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=anthropic_key)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert research assistant. Provide concise and accurate information."),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = []  # add tools here when you have them
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

raw_response = agent_executor.invoke(
    {"query": "Provide a summary of recent advancements in renewable energy technologies.", "name": "ResearchAgent"}
)
print(raw_response)