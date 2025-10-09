import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations = [
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    print("Hello from bd-ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    # contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    
    # system_prompt provides further instruction to model
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
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
        config=types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction=system_prompt
        ),
    )

    print(f"    Model: {model}")

    if verbose:
        print(f"    User prompt: {user_prompt}")

    if response.function_calls:
        for call in response.function_calls:
            print(f'    Calling function: {call.name}({call.args})')
    
    if response.text:
        print(f"    Response: {response.text.strip()}")

    if verbose:
        print(f"    Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"    Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
