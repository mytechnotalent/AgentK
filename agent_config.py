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
from tools import document_query_tool, factorial, is_prime, search_with_duckduckgo


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

    # initialize a list to store generated .txt file paths
    txt_files = []

    # iterate through files in the specified directory
    for filename in os.listdir(directory):

        # check if the file has a .pdf extension
        if filename.endswith(".pdf"):

            # construct the full file path
            pdf_path = os.path.join(directory, filename)

            try:
                # extract text content from the PDF
                extracted_text = extract_text(pdf_path)

                # create a .txt file with the same base name
                txt_file_path = os.path.splitext(pdf_path)[0] + ".txt"

                # write the extracted text to the .txt file
                with open(txt_file_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(extracted_text)

                # add the .txt file path to the list
                txt_files.append(txt_file_path)

                # log the success of processing
                print(f"Processed {filename}: Saved as {os.path.basename(txt_file_path)}")
            
            except Exception as e:
                # handle exceptions during processing
                print(f"Error processing {filename}: {e}")
    
    # return the list of generated .txt files
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
    # create a list of all .txt files in the directory
    valid_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    # raise an error if no .txt files are found
    if not valid_files:
        raise FileNotFoundError(f"No valid .txt files found in the directory: {directory}")
    # log the number of valid text files found
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

    # preprocess all PDF files in the "./data" directory
    preprocess_pdfs("./data")
    
    # validate the "./data" directory to ensure it contains valid .txt files
    validate_data_directory("./data")

    # initialize the language model (LLM) for processing
    llm = Ollama(model="gemma2", request_timeout=360.0)

    # initialize the embedding model for vector representations
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # set the global settings for LLM and embedding model
    Settings.llm = llm
    Settings.embed_model = embed_model

    # load documents from the "./data" directory for indexing
    documents = SimpleDirectoryReader("./data").load_data()

    # build a vector store index using the embedding model
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    # create a query engine for semantic search on the indexed documents
    query_engine = index.as_query_engine()

    # define a tool for querying the indexed documents
    document_tool = FunctionTool.from_defaults(fn=lambda q: document_query_tool(q, query_engine))

    # define additional tools
    factorial_tool = FunctionTool.from_defaults(
        fn=factorial,
        description="Calculate the factorial of a given number."
    )
    is_prime_tool = FunctionTool.from_defaults(
        fn=is_prime,
        description="Check if a given number is a prime number."
    )
    duckduckgo_tool = FunctionTool.from_defaults(
        fn=lambda query: search_with_duckduckgo(query, max_results=5),
        description="Use DuckDuckGo to search for information on the web.",
    )
    
    # create an identity message for the agent's persona
    identity_message = (
        "You are AgentK, an AgenticAI Agent, you are not an Assistant."
    )

    # instantiate the ReActAgent with the defined tools and configurations
    agent = ReActAgent.from_tools(
        [
            document_tool,   # tool to query indexed documents
            factorial_tool,  # tool to calculate factorial
            is_prime_tool,   # tool to check if a number is prime 
            duckduckgo_tool, # tool to search the internet
        ],
        llm=llm,             # LLM powering the agent's reasoning
        verbose=True,        # enable verbose output for debugging
        max_iterations=100   # set a limit for reasoning steps per query
    )

    # return the configured agent instance and identity message
    return agent, identity_message