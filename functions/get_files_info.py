import glob
import os
import unittest

def validate_is_jailed(a, b):
	'''
	Return True, if the absolute path of b is a sub-directory of a;
	otherwise, raise Exception

	Args:
		a (str): containing directory path
		b (str): contained directory path (relative path to a)

	Returns:
		True if b contained within a,
		or raise Exception with apropos message
	'''
	if os.path.commonpath([
		os.path.abspath(os.path.normpath(a)),
		os.path.abspath(os.path.normpath(os.path.join(a,b))),
		]) == os.path.abspath(os.path.normpath(a)):
		return True
	else:
		raise Exception(f'Cannot list "{b}" as it is outside the permitted working directory')

def validate_is_dir(a):
	'''
	Return True, if path a is a directory;
	otherwise, raise Exception

	Args:
		a (str): unvalidated directory path

	Returns:
		True a is a directory path,
		or raise Exception with apropos message
	'''
	if os.path.isdir(a):
		return True
	else:
		raise Exception(f'"{a}" is not a directory')

def get_files_info(working_directory, directory="."):
	norm_working_path = os.path.normpath(working_directory)
	norm_directory_path = os.path.normpath(
		os.path.join(working_directory, directory)
		)

	#	Result for current directory: -> directory = '.'
	#	Result for '{directory}' directory: -> directory is anything else
	if norm_working_path == norm_directory_path:
		directory_designation = "current"
	else:
		directory_designation = f"'{directory}'"

	response = f"Result for {directory_designation} directory:\n"
	
	# beware symbolic links and other path trickery
	try:
		# validate working_directory / directory lies within working_directory
		# or throw exception
		validate_is_jailed(working_directory, directory) 
		# validate norm_directory_path (directory we are listing) is a directory
		validate_is_dir(norm_directory_path)
	except Exception as e:
		return response + f"    Error: {e}\n"

	try:
		filenames = glob.glob(
			"*",
			root_dir=norm_directory_path
			)
	except Exception as e:
		return response + f"    Error: {e}\n"

	for filename in filenames:
		filepath = os.path.normpath(
			os.path.join(working_directory, directory, filename)
			)

		try:
			file_size = os.stat(filepath).st_size
			file_is_dir = os.path.isdir(filepath)
		except Exception as e:
	 		return response + f"    Error: {e}\n"

		path_info_string = f' - {filename}: file_size={file_size} bytes, is_dir={file_is_dir}\n'
		response += path_info_string

	return response