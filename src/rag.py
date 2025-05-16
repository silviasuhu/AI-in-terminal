import os
from langchain_openai import AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir, "../db", "chroma_db_commands")


def get_vector_store():

    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-small",
    )

    try:
        vector_store = Chroma(
            collection_name="commands",
            embedding_function=embeddings,
            persist_directory=persistent_dir,
        )
    except Exception as e:
        raise ValueError(
            f"Error initializing Chroma vector store: {e}. Ensure the directory exists and is accessible."
        )

    return vector_store
