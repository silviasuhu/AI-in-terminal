import os

from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from rag import get_vector_store, persistent_dir

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
commands_path = os.path.join(current_dir, "../data", "commands.txt")


def main():
    if os.path.exists(persistent_dir):
        print(
            f"Vector store already exists in {persistent_dir}. No need to initialize."
        )
        return

    print("Persistent directory doesn't exist. Initializing vector store...")

    # Ensure the text file exists
    if not os.path.exists(commands_path):
        print(f"Commands file not found at {commands_path}.")
        return

    # Read the text content from the file
    loader = TextLoader(commands_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    print("\n--- Document Chunks Information ---")
    print(f"Number of chunks: {len(docs)}")
    print(f"First chunk: {docs[0].page_content[:100]}...")

    print("\n--- Storing embeddings in Chroma ---")

    vector_store = get_vector_store()
    vector_store.add_documents(docs)


if __name__ == "__main__":
    main()
