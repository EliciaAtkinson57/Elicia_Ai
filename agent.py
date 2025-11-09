import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_with_agent(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Send a prompt to the OpenAI API and get a response.

    Args:
        prompt: The user's input message
        model: The OpenAI model to use (default: gpt-4o-mini)

    Returns:
        The AI's response text
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Main function to run the AI agent."""
    print("AI Agent Started! (Type 'quit' to exit)")
    print("-" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        print("\nAgent: ", end="", flush=True)
        response = chat_with_agent(user_input)
        print(response)


if __name__ == "__main__":
    main()
