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

from duckduckgo_search import DDGS


def search_with_duckduckgo(query, max_results=5):
    """
    Perform a DuckDuckGo search using DDGS and return a list of results.

    Args:
        query (str): The search query string to be submitted to DuckDuckGo.
        max_results (int): Maximum number of results to return (default is 5).

    Returns:
        list[dict]: A list of search results, where each result is represented as a dictionary 
                    containing metadata such as the title, link, and snippet of the search result.

    Raises:
        ImportError: If the `duckduckgo_search` package is not installed.
        Exception: If an unexpected error occurs during the search process.
    """
    
    # initialize an empty list to store search results
    results = []
    
    # create a DuckDuckGo search instance using the DDGS context manager
    with DDGS() as ddgs:

        # perform a search query and iterate through the results
        for result in ddgs.text(query, region="wt-wt", safesearch="Off", timelimit="y"):
            
            # append each result to the results list
            results.append(result)
            
            # stop the search once the max_results limit is reached
            if len(results) >= max_results:
                break
    
    # return the list of search results
    return results
