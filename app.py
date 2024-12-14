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

from flask import Flask, render_template, request
from agent_config import configure_agent

# create an instance of the Flask application
app = Flask(__name__)

# configure the agent and fetch its identity message
agent, identity_message = configure_agent()


@app.route("/")
def index():
    """
    Render the home page.

    This function handles the root route ("/") of the Flask app. It renders
    the `index.html` template, which serves as the landing page for the
    application.

    Returns:
        str: Rendered HTML content for the home page.
    """

    # render the index.html file located in the templates folder
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query_agent():
    """
    Handle user queries and return agent responses.

    This function processes user queries sent via the POST request to the "/query" route.
    It retrieves the user's query from the form data, processes it using the agent,
    and returns the agent's response as a JSON object.

    Returns:
        tuple: JSON response containing the agent's response and an HTTP status code.
    """

    # retrieve the user's query from the form data
    user_query = request.form.get("query", "").strip()

    # if the query is empty, return a 400 Bad Request response with an error message
    if not user_query:
        return {"response": "I didn't catch that. Could you please repeat?"}, 400

    try:
        # construct the full query to include the agent's identity message
        full_query = f"{identity_message}\n\nUser: {user_query}"

        # pass the query to the agent's chat method and get the response
        response = agent.chat(full_query)

        # convert the response to a string (if not already) and send it back
        response_text = str(response)
        return {"response": response_text}, 200

    except Exception as e:
        # if an error occurs, return a 500 Internal Server Error response
        # with a helpful error message
        return {"response": f"An error occurred while processing your request: {e}"}, 500


if __name__ == "__main__":
    # run the Flask application in debug mode
    app.run(debug=True, port=5001)