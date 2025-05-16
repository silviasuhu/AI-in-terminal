import os
import subprocess
import sys
import re
import requests


from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent


load_dotenv()


@tool
def get_git_branch():
    """Get the current Git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error: Could not get current Git branch.")
        print(e.stderr)
        sys.exit(1)


@tool
def get_jira_ticket():
    """Get the jira ticket."""
    try:
        branch_name = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
        )
        match = re.search(r"[A-Z]+-\d+", branch_name.stdout.strip())
        if match:
            return match.group(0)
        else:
            return "This directory does not have a Jira ticket."
    except subprocess.CalledProcessError as e:
        print("Error: Could not get Jira ticket.")
        print(e.stderr)
        sys.exit(1)


@tool
def get_jira_instance_url():
    """Get the Jira instance url to get the url to a jira ticket."""
    return os.getenv("JIRA_ENDPOINT")


@tool
def get_jira_info():
    """Get the information of the jira ticket associated to the current directory."""

    JIRA_API_BASE_URL = "https://jira.mongodb.org/rest/api/2/issue/"

    try:
        jira_ticket = ""
        branch_name = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
        )
        match = re.search(r"[A-Z]+-\d+", branch_name.stdout.strip())
        if match:
            jira_ticket = match.group(0)
        else:
            return "This directory does not have a Jira ticket."

        url = f"{JIRA_API_BASE_URL}{jira_ticket}"
        response = requests.get(url)

        if response.ok:
            return response.json()
        else:
            print("Response not OK")
            return "It has not been posible to fetch the information from the Jira API."

    except subprocess.CalledProcessError as e:
        print("Error: Could not get Jira ticket.")
        print(e.stderr)
        sys.exit(1)


def ask_env_question_to_llm(query):

    llm = AzureChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0,
        api_version="2024-12-01-preview",
    )

    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                "You are a helpul assistant. Say don't know if you don't know the answer.",
            ),
            (
                "human",
                "{input}\n\nThoughts: {agent_scratchpad}",
            ),
        ]
    )

    tools = [
        get_git_branch,
        get_jira_ticket,
        get_jira_info,
        get_jira_instance_url,
    ]
    agent = create_tool_calling_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    response = agent_executor.invoke({"input": query})

    return response["output"]
