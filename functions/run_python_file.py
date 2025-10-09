import os
import subprocess

from google import genai
from google.genai import types

from functions.config import COMMAND_TIMEOUT
from functions.validation import validate_is_jailed

schema_run_python_file = types.FunctionDeclaration(
	name="run_python_file",
	description="Run python source file at specified path, relative to the working directory. A list of arguments can be provided.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path of the python source file to run, relative to the working directory.",
			),
			"args": types.Schema(
				type=types.Type.ARRAY,
				description="A list of arguments to pass to the python runtime.",
				items=types.Schema(
					type=types.Type.STRING,
				),
			),
		}
	)
)

def run_python_file(working_directory, file_path, args=[]):
	norm_working_path = os.path.normpath(working_directory)
	norm_file_path = os.path.normpath(
		os.path.join(working_directory, file_path)
		)

	try:
		# validate working_directory / file_path lies within working_directory
		# or throw exception
		validate_is_jailed(working_directory, file_path, "execute")
		# validate file_path exists and is a file
		if not os.path.isfile(norm_file_path):
			raise Exception(f'Error: File "{file_path}" not found.')
		# ensure file_path has .py extension (no guarantee of code, but)
		if not file_path.endswith('.py'):
			raise Exception(f'Error: "{file_path}" is not a Python file.')
	except Exception as e:
		print(f'Error: {e}')

	try:
		result = subprocess.run(
			['python3', file_path],
			*args,
			capture_output=True,
			cwd=norm_working_path,
			timeout=COMMAND_TIMEOUT,
			)
	except Exception as e:
		return (f'Error: executing Python file: {e}')

	return_string = ''
	return_string += f'STDOUT: {result.stdout}\n'
	return_string += f'STDERR: {result.stderr}\n'
	if result.returncode != 0:
		return_string += f'Process exited with code {result.returncode}\n'
	if len(result.stderr) == 0:
		return_string += f'No output produced\n'

	return return_string