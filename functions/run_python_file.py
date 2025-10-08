import os
import subprocess

from functions.validation import validate_is_jailed

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