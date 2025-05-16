import os
import sys
import logging

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from rag import get_vector_store
from agent_llm import ask_env_question_to_llm
from basic_llm import ask_generic_question_to_llm, ask_command_to_llm


load_dotenv()

# Silent the logging from langchain and chromadb
logging.getLogger("chromadb").setLevel(logging.ERROR)
logging.getLogger("langchain").setLevel(logging.ERROR)


def main():

    if len(sys.argv) < 3:
        print("Usage: python main.py <query> <base_dir>")
        sys.exit(1)

    query = sys.argv[1]
    base_dir = sys.argv[2]

    IS_GENERIC_QUESTION = query.startswith("Q ")
    IS_ENVIRONMENT_QUESTION = query.startswith("E ")
    IS_COMMAND_REQUEST = not IS_GENERIC_QUESTION and not IS_ENVIRONMENT_QUESTION

    if IS_GENERIC_QUESTION or IS_ENVIRONMENT_QUESTION:
        query = query[2:]

    # Change the directory to base_dir
    original_dir = os.getcwd()
    os.chdir(base_dir)
    try:
        if IS_COMMAND_REQUEST:
            response = ask_command_to_llm(query)

        elif IS_GENERIC_QUESTION:
            response = ask_generic_question_to_llm(query)

        elif IS_ENVIRONMENT_QUESTION:
            response = ask_env_question_to_llm(query)

    finally:
        os.chdir(original_dir)

    print(response)


if __name__ == "__main__":
    main()
