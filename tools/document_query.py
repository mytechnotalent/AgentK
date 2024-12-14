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


def document_query_tool(query: str, query_engine) -> str:
    """
    Perform a semantic search query on the indexed documents.

    This function takes a user query string and a query engine, which is 
    typically created from a vector store index. It performs a search on the 
    indexed documents and retrieves the most relevant response.

    Args:
        query (str): The query string entered by the user.
        query_engine: An instance of a query engine, created from the document 
                      vector store index. The query engine is responsible for 
                      performing semantic searches on the indexed documents.

    Returns:
        str: The response to the query, converted to a string format. The response 
             usually contains the most relevant document or passage from the index 
             based on the semantic similarity to the query.
    """

    # perform the query on the document index
    response = query_engine.query(query)  #
    
    # convert the response to a string and return
    return str(response)  