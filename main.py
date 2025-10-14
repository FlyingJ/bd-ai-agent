import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.config import MAX_AGENT_ITERATIONS, SYSTEM_PROMPT

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations = [
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)

function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    
    function_args['working_directory'] = 'calculator'

    if verbose:
        print(f'Calling function: {function_name}({function_args})')
    else:
        print(f' - Calling function: {function_name}')

    try:
        function_result = function_map[function_name](**function_args)
    except KeyError:
        return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={'error': f'Unknown function: {function_name}'},
                )
            ],
        )

    return types.Content(
        role='tool',
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={'result': function_result},
            )
        ]
    )

def main():
    print("Hello from bd-ai-agent!")

    # read in API key via environment variable
    # the client will use the key to make calls to the AI API
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # specify the model to use
    model = "gemini-2.0-flash-001"
    print(f"    Model: {model}")

    # this seems a janky way of dealing with verbosity and arguments in general
    # perhaps the user prompt should be read in from a file or command line
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
    if verbose:
        print(f"    User prompt: {user_prompt}")

    # seed messages list with user supplied prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    agent_iterations = 0
    while agent_iterations < MAX_AGENT_ITERATIONS:
        agent_iterations += 1

        # send updated messages to model and save response
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools = [available_functions],
                system_instruction=SYSTEM_PROMPT
            ),
        )

        # if response makes function calls
        # call the functions
        # Q: update messages with response?
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=True)
                if not function_call_result.parts[0].function_response.response:
                    raise Exception(f'    Error: failed to call function: "{function_call.name}"')
                elif verbose:
                    print(f' -> {function_call_result.parts[0].function_response.response}')

        # still doing stuff
        # update messages and iterate
        
        # if no new function call and only text response, we are done
        # jump out of the loop
        if response.text:
            print(f"    Response: {response.text.strip()}")
            break

        # if verbose:
        #     print(f"    Prompt tokens: {response.usage_metadata.prompt_token_count}")
        #     print(f"    Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
