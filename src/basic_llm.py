import os
import subprocess

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from rag import get_vector_store

load_dotenv()


def ask_command_to_llm(query):

    def get_machine_info():
        result = subprocess.run(["uname", "-sm"], capture_output=True, text=True)
        return result.stdout.strip()

    shell = os.environ.get("SHELL")
    machine = get_machine_info()

    llm = AzureChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0,
        api_version="2024-12-01-preview",
    )

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 3,
        }
    )

    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                (
                    "Return commands suitable for copy/pasting into shell '{shell}' on machine '{machine}'. "
                    "Do NOT include commentary or Markdown triple-backtick code blocks, "
                    "as your whole response will be copied into my terminal automatically. "
                    "Say don't know if you don't know the answer.\n\n"
                    "This is a list of information that define what are the commands I personally use:\n"
                    "<info>\n"
                    "{context}\n"
                    "</info>"
                ),
            ),
            ("human", "The command/s should do this: {query}"),
        ]
    )

    combine_docs_chain = create_stuff_documents_chain(llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    # Get the response from the LLM
    response = rag_chain.invoke(
        {
            "input": "hola",
            "query": query,
            "shell": shell,
            "machine": machine,
        }
    )

    return response["answer"]


def ask_generic_question_to_llm(query):

    llm = AzureChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0,
        api_version="2024-12-01-preview",
    )

    prompt_template = ChatPromptTemplate(
        [
            ("system", "You are a helpful assistant.\n"),
            ("human", "{query}"),
        ]
    )
    prompt = prompt_template.invoke(
        {
            "query": query,
        }
    )

    response = llm.invoke(prompt)

    return response.content
