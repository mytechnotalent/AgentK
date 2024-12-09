def document_query_tool(query: str, query_engine) -> str:
    """Query the indexed documents."""
    
    response = query_engine.query(query)
    return str(response)