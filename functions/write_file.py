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
		with open(norm_file_path) as fd:
			file_content = fd.read(MAX_CHARS)

		# let the caller know that we needed to truncate at MAX_CHARS
		if len(file_content) >= MAX_CHARS:
			file_footer = f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
			file_content += file_footer
	
		return response_header + file_content
	except Exception as e:
		return response_header + f"    Error: {e}\n"