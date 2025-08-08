import os

from pathlib import Path

def get_files_info(working_directory, directory="."):
	wd = Path(working_directory)
	td = wd / directory

	def validate_is_jailed(wd, td):
		if wd in td.parents:
			return True
		else:
			raise Exception(f'Error: Cannot list "{td}" as it is outside the permitted working directory')

	def validate_is_dir(td):
		if td.is_dir():
			return True
		else:
			raise Exception(f'Error: "{td}" is not a directory')

	try:
		# validate absolute_directory lies within absolute_working_directory or throw exception
		validate_is_jailed(wd, td) 
		# validate absolute_directory is a directory
		validate_is_dir(td)
	except Exception as e:
		return e

	# FIX: this "redefinition" seems unnecessary
	directory = Path(directory)

	response = ''
	
	try:
		filenames = directory.glob('*')
	except Exception as e:
		return f"Error: {e}"

	for filename in filenames:
		path = directory / filename
		
		try:
			file_size = path.stat().st_size
		except Exception as e:
			return f"Error: {e}"

		try:
			file_is_dir = path.is_dir()
		except Exception as e:
			return f"Error: {e}"

		path_info_string = f'- {filename}: file_size={file_size} bytes, is_dir={file_is_dir}\n'
		response += path_info_string

	return response