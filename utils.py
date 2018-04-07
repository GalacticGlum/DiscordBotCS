import os

"""
Read the contents of a file.

Args:
    filepath: The path of the file to read.
    mode: The mode to read the file in (defaults to read).

Returns:
    The contents of the file at the specified path.

Raises:
   OSError: if the file cannot be opened. 
"""
def get_file(filepath, mode='r'):
    with open(filepath, mode=mode) as file:
        return file.read()