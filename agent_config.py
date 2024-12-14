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

from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import SimpleDirectoryReader
from tools import factorial, is_prime, document_query_tool


def configure_agent():
    """
    Configure and return the AgentK instance along with its identity message.

    This function sets up the necessary components for AgentK:
    1. Initializes the language model (LLM) and embedding model.
    2. Loads documents and creates a vector store index for efficient querying.
    3. Defines tools for AgentK to use (e.g., factorial, is_prime, and document query).
    4. Sets up AgentK as a ReActAgent with the specified tools and configurations.

    Returns:
        tuple:
            - agent (ReActAgent): The configured agent instance.
            - identity_message (str): The identity message for the agent.
    """

    # initialize the language model (LLM) with a specific model name and timeout
    llm = Ollama(model="mixtral:8x7b", request_timeout=360.0)

    # initialize the embedding model for vector representations
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # set LLM and embedding model globally in the settings
    Settings.llm = llm
    Settings.embed_model = embed_model

    # load documents from the "./data" directory
    # these documents will be indexed for semantic search
    documents = SimpleDirectoryReader("./data").load_data()

    # build a vector store index from the loaded documents using the embedding model
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    # create a query engine from the vector store index for document searches
    query_engine = index.as_query_engine()

    # instantiate tools
    document_tool = FunctionTool.from_defaults(fn=lambda q: document_query_tool(q, query_engine))
    factorial_tool = FunctionTool.from_defaults(fn=factorial)
    is_prime_tool = FunctionTool.from_defaults(fn=is_prime)
    
    # define the agent's identity message
    # this message provides context about the agent's persona and capabilities
    identity_message = (
        "You are AgentK, an AgenticAI Agent, you are not an Assistant."
    )

    # instantiate the ReActAgent with the defined tools and configurations
    # the ReActAgent is designed to reason, act, and use tools iteratively to respond
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

    # return the configured agent and its identity message
    return agent, identity_message