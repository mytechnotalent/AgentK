from agent_config import configure_agent

# List of valid exit commands
EXIT_COMMANDS = ["goodbye", "bye", "exit", "quit", "stop"]

def run_agent():
    """Run AgentK with text input and document retrieval."""

    # Configure the agent
    agent, identity_message = configure_agent()

    try:
        while True:
            # Prompt user for input
            query = input("enter your query (or type 'goodbye' to exit): ").strip()

            # Exit if the user types goodbye or another exit command
            if query.lower() in EXIT_COMMANDS:
                print("Goodbye!")
                break

            # Handle parsing issues
            if not query:
                print("I didn't catch that. Could you please repeat?")
                continue

            # Pass query to agent
            full_query = f"{identity_message}\n\nUser: {query}"
            print(f"Query Passed to Agent: {query}")  # Debugging log

            try:
                # Agent processes the full query and generates a response
                response = agent.chat(full_query)
                response_text = str(response)  # Extract plain text from the response
                print(f"AgentK: {response_text}")
            except Exception as e:
                # Handle any errors during the agent's query processing
                print(f"an error occurred: {e}")
                print("An error occurred while processing your request. Please try again.")
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    # Run the agent
    run_agent()