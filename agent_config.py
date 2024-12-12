from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import SimpleDirectoryReader
from tools import factorial, is_prime, document_query_tool


def configure_agent():
    """Configure and return the AgentK instance."""
    # Initialize LLM and embedding models
    llm = Ollama(model="mixtral:8x7b", request_timeout=360.0)
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = llm
    Settings.embed_model = embed_model

    # Load documents and build index
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    query_engine = index.as_query_engine()

    # Instantiate tools
    factorial_tool = FunctionTool.from_defaults(fn=factorial)
    is_prime_tool = FunctionTool.from_defaults(fn=is_prime)
    document_tool = FunctionTool.from_defaults(fn=lambda q: document_query_tool(q, query_engine))

    # Create agent identity
    identity_message = (
        "You are AgentK, an AgenticAI Agent, you are not an Assistant."
    )

    # Instantiate agent
    agent = ReActAgent.from_tools(
        [
            factorial_tool,
            is_prime_tool,
            document_tool,
        ],
        llm=llm,
        verbose=True,
        max_iterations=100,
    )

    return agent, identity_message