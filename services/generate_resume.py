import functools
import operator
import requests # type: ignore
import os
from bs4 import BeautifulSoup # type: ignore
from duckduckgo_search import DDGS # type: ignore
from langchain.agents import AgentExecutor, create_openai_tools_agent # type: ignore
from langchain_core.messages import HumanMessage, BaseMessage # type: ignore
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser # type: ignore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # type: ignore
from langgraph.graph import StateGraph, END 
from langchain.tools import tool # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from typing import TypedDict, Annotated, Sequence



from langchain.tools import tool  # Ensure you've correctly imported the tool decorator

@tool("profile_content", return_direct=False)
def get_profile_content(profile_content):
    """Extracts and processes profile content data from a text input."""
    profileContent = profile_content.split(',')  # Assuming profile_content is a string of text
    return profileContent

@tool("job_desc_content", return_direct=False)
def get_job_desc_content(job_desc_content):
    """Extracts and processes job description content data from a text input."""
    jobDescContent = job_desc_content.split(',')  # Assuming job_desc_content is a string of text
    return jobDescContent



def create_agents(llm: ChatOpenAI,
                  tools: list,
                  system_prompt: str) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

