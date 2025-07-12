import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    print("Hello from bd-ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    # contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    user_prompt = ' '.join(sys.argv[1:])
    if len(user_prompt) < 3:
        print("Error: no prompt provided")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model=model,
        contents=messages,
    )

    print(f"""
        Model: {model}
        Prompt: {contents}
        Response: {response.text}
        Prompt tokens: {response.usage_metadata.prompt_token_count}
        Response tokens: {response.usage_metadata.candidates_token_count}
        """)

if __name__ == "__main__":
    main()
