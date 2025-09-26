import os

from functions.config import MAX_CHARS
from functions.validation import validate_is_jailed, validate_is_file

def get_file_content(working_directory, file_path):
	norm_working_path = os.path.normpath(working_directory)
	norm_file_path = os.path.normpath(
		os.path.join(working_directory, file_path)
		)

	response_header = f'Result for "{file_path}":\n'

	try:
		# validate working_directory / directory lies within working_directory
		# or throw exception
		validate_is_jailed(working_directory, file_path, "read") 
		# validate norm_directory_path (directory we are listing) is a directory
		validate_is_file(norm_file_path)
	
		# read first MAX_CHARS of file_path and return
		with open(norm_file_path) as fd:
			file_content = fd.read(MAX_CHARS)

		# let caller know file truncated at MAX_CHARS
		if len(file_content) >= MAX_CHARS:
			file_footer = f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
			file_content += file_footer
	
		return response_header + file_content
	except Exception as e:
		return response_header + f"    Error: {e}\n"
