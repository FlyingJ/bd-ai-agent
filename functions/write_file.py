import os

from functions.validation import validate_is_file, validate_is_jailed

def write_file(working_directory, file_path, content):
	norm_working_path = os.path.normpath(working_directory)
	norm_file_path = os.path.normpath(
		os.path.join(working_directory, file_path)
		)
	
	try:
		# validate working_directory / directory lies within working_directory
		# or throw exception
		validate_is_jailed(working_directory, file_path, "write")
		# create target file directory, if absent
		dest_path = os.path.dirname(norm_file_path)
		if not os.path.isdir(dest_path):
			os.makedirs(dest_path)
	
		# write content to file
		with open(norm_file_path, "w", encoding="utf-8") as fd:
			chars_written = fd.write(content)

		# return status
		if len(content) == chars_written:
			return f'Successfully wrote to "{file_path}" ({chars_written} characters written)'
		else:
			raise Exception(f'Write to "{file_path}" incomplete: {chars_written} of {len(content)} characters written')
	except Exception as e:
		return f'    Error: {e}\n'