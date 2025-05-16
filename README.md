# AI-in-terminal

A command-line tool that uses LLMs (Large Language Models) to answer questions and retrieve commands, with support for retrieval-augmented generation (RAG) and persistent vector storage using ChromaDB.

## Features

- Ask generic questions, environment-specific questions, or request commands.
- Uses Azure OpenAI for LLM responses.
- Stores and retrieves command documentation using ChromaDB and LangChain.
- Easily extensible with new commands and documents.

## Setup

1. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Install `fzf` (required for shell integration):**

   On macOS, you can use Homebrew:

   ```sh
   brew install fzf
   ```

   For other platforms or installation methods, see: https://github.com/junegunn/fzf

3. **Configure environment variables:**

   Copy `.env.example` to `.env` and fill in your Azure OpenAI and JIRA credentials.

4. **Prepare the vector store:**

   Make sure to fill `data/commands.txt` with your command documentation before running the following command:

   ```sh
   python src/main_load_commands.py
   ```

   This will load and embed the commands from `data/commands.txt` into ChromaDB located in ./db.

5. **Add shell integration:**

   Add the following line to your `.bashrc` (or `.zshrc`) to enable the `ask_llm` shell function:

   ```sh
   source <root_directory_of_this_project>/bash/ask_llm.sh
   ```

## Usage

You can use AI-in-terminal in two ways:

### 1. Shell Integration (recommended)

After completing step 4 of the setup, you can access an interactive prompt from your terminal by pressing `Ctrl+K`.  

- To ask a generic question: Prefix your query with `Q `  

- To ask an environment question: Prefix your query with `E `  

- To request a command (no prefix needed):  

This integration allows you to quickly ask questions or retrieve commands directly from your shell, streamlining your workflow.

### 2. Direct Python Script

Run the main script with your query and the base directory:

```sh
python src/main_llm.py "<query>" <base_dir>
```

- To ask a generic question:  
  Prefix your query with `Q `  
  Example: `python src/main_llm.py "Q What is a vector store?" .`

- To ask an environment question:  
  Prefix your query with `E `  
  Example: `python src/main_llm.py "E How do I set up my environment?" .`

- To request a command (no prefix needed):  
  Example: `python src/main_llm.py "build mongodb" .`

## Adding Commands

The LLM uses a Retrieval-Augmented Generation (RAG) mechanism to retrieve your non-generic commands.  
When you add new command documentation to [`data/commands.txt`](data/commands.txt), the content is embedded as vectors and stored locally in a Chroma database. This allows the LLM to efficiently search and suggest relevant commands based on your queries.

To update the command database:

1. Edit [`data/commands.txt`](data/commands.txt) to add or modify command documentation.
2. Remove the existing vector store directory:
   ```sh
   rm -rf db/chroma_db_commands
   ```
3. Reload the commands into the vector store:
   ```sh
   python src/main_load_commands.py
   ```
