import os

def write_file(working_directory, file_path, content):
	norm_working_path = os.path.normpath(working_directory)
	norm_file_path = os.path.normpath(
		os.path.join(working_directory, file_path)
		)
	
	try:
		# validate working_directory / directory lies within working_directory
		# or throw exception
		validate_is_jailed(working_directory, file_path)
		# validate norm_directory_path (directory we are listing) is a directory
		validate_is_file(norm_file_path)
	
		# read first MAX_CHARS of file_path and return
		with open(norm_file_path, "r", encoding="utf-8") as fd:
			chars_written = fd.write(content)

		# let the caller know that we needed to truncate at MAX_CHARS
		if len(content) != chars_written:
			return f'Successfully wrote to "{file_path}" ({chars_written} characters written)'
		else:
			raise Exception(f'Write to "{file_path}" incomplete: {chars_written} of {len(content)} characters written')
	except Exception as e:
		return f'    Error: {e}\n'