import json
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

class EmailAnalysis(BaseModel):
    category: str = Field(description="Main category of the email")
    priority: str = Field(description="Priority level: low, medium, or high")
    summary: str = Field(description="Short summary of the email")
    requested_action: str = Field(description="What action the sender wants")
    requested_date: str | None = Field(default=None, description="Date mentioned in the email, if any")
    requested_time: str | None = Field(default=None, description="Time mentioned in the email, if any")
    sentiment: str = Field(description="Sentiment: positive, neutral, or negative")

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

structured_llm = llm.with_structured_output(EmailAnalysis)

def analyze_email(email_text: str) -> dict:
    prompt = f"""
You are an assistant that analyzes business emails.

Read the email and extract:
- category
- priority
- summary
- requested_action
- requested_date
- requested_time
- sentiment

Rules:
- category must be something practical like: support, sales, billing, meeting, complaint, HR
- priority must be only: low, medium, high
- if there is no date, return null
- if there is no time, return null
- summary must be short and clear
- requested_action should explain what the sender wants
- sentiment must be: positive, neutral, or negative

Email:
{email_text}
"""

    result = structured_llm.invoke([HumanMessage(content=prompt)])
    return result.model_dump()

def save_result(result: dict, path: str = "outputs/parsed_emails.json") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")