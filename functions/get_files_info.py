import os

from pathlib import Path

def get_files_info(working_directory, directory="."):
	wd = Path(working_directory)
	td = wd / directory

	# validate absolute_directory lies within absolute_working_directory or throw exception
	if wd not in td.parents:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	# validate absolute_directory is a directory
	if not td.is_dir():
		return f'Error: "{directory}" is not a directory'

	directory = Path(directory)

	response = ''
	for filename in directory.glob('*'):
		path = directory / filename
		path_info_string = f'- {filename}: file_size={path.stat().st_size} bytes, is_dir={path.is_dir()}\n'
		response += path_info_string

	return response