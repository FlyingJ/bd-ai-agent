import os

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

def validate_is_file(a):
	'''
	Return True if path a is a file;
	otherwise raise Exception

	Args:
		a (str): unvalidated file path

	Returns:
		True a is a file path,
		or raise Exception with apropos message
	'''
	if os.path.isfile(a):
		return True
	else:
		raise Exception(f'File not found or is not a regular file: "{a}"')