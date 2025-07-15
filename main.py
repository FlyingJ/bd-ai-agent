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
    
    verbose = False
    if sys.argv[-1] == "--verbose":
        verbose = True
        #print(f'{sys.argv[0]}: verbose output set')
        # FIXME
        # remove the verbose arg to keep user_prompt happy
        sys.argv.pop()

    if len(sys.argv) != 2:
        print("Error: no prompt provided")
        sys.exit(1)

    user_prompt = sys.argv.pop()

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model=model,
        contents=messages,
    )

    print(f"    Model: {model}")

    if verbose:
        print(f"    User prompt: {user_prompt}")

    print(f"    Response: {response.text.strip()}")

    if verbose:
        print(f"    Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"    Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
