# I am going to build a simple file handling module that allows me to read, write, and append to files. I will also include error handling to manage cases where the file may not exist or there are issues with permissions.

def read_file(file_path):
    """Reads the content of a file and returns it as a string."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file '{file_path}' does not exist."
    except PermissionError:
        return f"Error: You do not have permission to read the file '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def write_file(file_path, content):
    """Writes the given content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Content successfully written to '{file_path}'."
    except PermissionError:
        return f"Error: You do not have permission to write to the file '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def append_to_file(file_path, content):
    """Appends the given content to a file."""
    try:
        with open(file_path, 'a') as file:
            file.write(content)
        return f"Content successfully appended to '{file_path}'."
    except PermissionError:
        return f"Error: You do not have permission to append to the file '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example usage:

# print(read_file('example.txt'))
# print(write_file('example.txt', 'Hello, World!'))
print(append_to_file('example.txt', '\nThis is an appended line.'))
