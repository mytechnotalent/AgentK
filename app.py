from flask import Flask, render_template, request
from agent_config import configure_agent

app = Flask(__name__)

# Configure the agent
agent, identity_message = configure_agent()

@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query_agent():
    """Handle user queries and return agent responses."""
    user_query = request.form.get("query", "").strip()

    if not user_query:
        return {"response": "I didn't catch that. Could you please repeat?"}, 400

    try:
        # Pass query to the agent
        full_query = f"{identity_message}\n\nUser: {user_query}"
        response = agent.chat(full_query)
        response_text = str(response)
        return {"response": response_text}, 200
    except Exception as e:
        return {"response": f"An error occurred while processing your request: {e}"}, 500

if __name__ == "__main__":
    app.run(debug=True)