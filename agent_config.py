# MIT License

# Copyright (c) 2024 My Techno Talent

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import SimpleDirectoryReader
from pdfminer.high_level import extract_text
from tools import factorial, is_prime, document_query_tool


def preprocess_pdfs(directory: str):
    """
    Preprocess PDF documents in a directory by converting them to text files.
    
    This function reads all PDF files in the specified directory, extracts text content from them,
    and saves the extracted text as .txt files in the same directory.

    Args:
        directory (str): The path to the directory containing PDF files.

    Returns:
        list[str]: A list of paths to the generated .txt files.
    """
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            try:
                # Extract text from the PDF
                extracted_text = extract_text(pdf_path)
                # Create a .txt file with the same base name
                txt_file_path = os.path.splitext(pdf_path)[0] + ".txt"
                with open(txt_file_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(extracted_text)
                txt_files.append(txt_file_path)
                print(f"Processed {filename}: Saved as {os.path.basename(txt_file_path)}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return txt_files


def validate_data_directory(directory: str):
    """
    Validate the data directory to ensure it contains parseable text files.

    This function checks the specified directory for text files. If no valid files
    are found, it raises an error to alert the user.

    Args:
        directory (str): The path to the data directory to validate.

    Raises:
        FileNotFoundError: If no valid .txt files are found in the directory.
    """

    valid_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    if not valid_files:
        raise FileNotFoundError(f"No valid .txt files found in the directory: {directory}")
    print(f"Data directory validated: {len(valid_files)} text files found.")


def configure_agent():
    """
    Configure and return the AgentK instance along with its identity message.

    This function sets up the necessary components for AgentK:
    1. Preprocesses PDF documents in the "./data" directory to ensure parseability.
    2. Validates the "./data" directory to confirm the presence of valid text files.
    3. Initializes the language model (LLM) and embedding model.
    4. Loads documents and creates a vector store index for efficient querying.
    5. Defines tools for AgentK to use (e.g., factorial, is_prime, and document query).
    6. Sets up AgentK as a ReActAgent with the specified tools and configurations.

    Returns:
        tuple:
            - agent (ReActAgent): The configured agent instance.
            - identity_message (str): The identity message for the agent.
    """

    # Preprocess PDF documents in the "./data" directory
    preprocess_pdfs("./data")
    
    # Validate the data directory
    validate_data_directory("./data")

    # Initialize the language model (LLM) with a specific model name and timeout
    llm = Ollama(model="mixtral:8x7b", request_timeout=360.0)

    # Initialize the embedding model for vector representations
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Set LLM and embedding model globally in the settings
    Settings.llm = llm
    Settings.embed_model = embed_model

    # Load documents from the "./data" directory
    # These documents will be indexed for semantic search
    documents = SimpleDirectoryReader("./data").load_data()

    # Build a vector store index from the loaded documents using the embedding model
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    # Create a query engine from the vector store index for document searches
    query_engine = index.as_query_engine()

    # Instantiate tools
    document_tool = FunctionTool.from_defaults(fn=lambda q: document_query_tool(q, query_engine))
    factorial_tool = FunctionTool.from_defaults(fn=factorial)
    is_prime_tool = FunctionTool.from_defaults(fn=is_prime)
    
    # Define the agent's identity message
    # This message provides context about the agent's persona and capabilities
    identity_message = (
        "You are AgentK, an AgenticAI Agent, you are not an Assistant."
    )

    # Instantiate the ReActAgent with the defined tools and configurations
    # The ReActAgent is designed to reason, act, and use tools iteratively to respond
    agent = ReActAgent.from_tools(
        [
            document_tool,   # tool to query indexed documents
            factorial_tool,  # tool to calculate factorial
            is_prime_tool,   # tool to check if a number is prime 
        ],
        llm=llm,             # the LLM that powers the agent's reasoning
        verbose=True,        # enable verbose logging for debugging
        max_iterations=100   # limit the number of reasoning steps per query
    )

    # Return the configured agent and its identity message
    return agent, identity_message