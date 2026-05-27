from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv()

# =========================
# GROQ API KEY SETUP
# =========================

GROQ_KEYS = [k.strip() for k in os.getenv("GROQ_API_KEYS").split(",")]


def get_working_llm():
    last_error = None

    for key in GROQ_KEYS:
        try:
            llm = ChatGroq(
                api_key=key,
                model="llama-3.3-70b-versatile",
                temperature=0
            )

            llm.invoke("hello")

            print(f"Using Groq key: {key[:10]}...")
            return llm

        except Exception as e:
            print(f"Groq key failed, trying next... {e}")
            last_error = e

    raise Exception(f"All Groq API keys failed: {last_error}")


llm = get_working_llm()

# =========================
# SEARCH AGENT
# =========================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


# =========================
# READER AGENT
# =========================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# =========================
# WRITER CHAIN
# =========================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured, detailed, insightful, and factual research reports."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

1. Introduction
2. Key Findings (minimum 3 detailed points)
3. Conclusion
4. Sources (list all URLs found in the research)

Rules:
- Be factual
- Be professional
- Avoid repetition
- Use clear formatting
- Expand explanations where needed
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# =========================
# CRITIC CHAIN
# =========================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a strict and constructive research critic. Review reports honestly and provide actionable improvements."
    ),
    (
        "human",
        """Review the research report below strictly.

Report:
{report}

Respond EXACTLY in this format:

Score: X/10

Strengths:
- point 1
- point 2
- point 3

Areas to Improve:
- point 1
- point 2
- point 3

One line verdict:
your verdict
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()