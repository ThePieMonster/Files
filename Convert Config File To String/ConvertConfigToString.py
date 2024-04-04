"""
Converts the content of a configuration file into a single string with explicit escape sequences for newline characters,
optionally removes all single quote characters, and writes the result to an output file.

This script reads the entire content of a specified file, replaces all types of newline characters (\r\n for Windows,
\n for Unix/Linux, and \r for older Mac) with their corresponding literal escape sequences (\\r\\n, \\n, and \\r), optionally
removes all single quote characters if the --remove-single-quotes flag is provided, and writes the modified content to a specified
output file. The goal is to represent the file's content, including newlines and optionally without single quotes,
as a single-line string. This can be particularly useful for configurations or data that need to be transmitted or processed
in environments that require single-line input.

Parameters:
    --input <path_to_config_file> : Specifies the path to the configuration file to be converted.
    --output <path_to_output_file> : Specifies the path where the converted string will be saved.
    --remove-single-quotes : If provided, all single quote characters (') in the file's content will be removed.

\r = CR (Carriage Return) → Used as a new line character in Mac OS before X
\n = LF (Line Feed) → Used as a new line character in Unix/Mac OS X
\r\n = CR + LF → Used as a new line character in Windows

Usage:
    python ConvertConfigToString.py --input <path_to_config_file> --output <path_to_output_file> [--remove-single-quotes]

Example:
    python ConvertConfigToString.py --input C:/path/to/your/config.file --output C:/path/to/output.txt --remove-single-quotes
"""

import argparse
from pathlib import Path

def read_file_to_string(file_path):
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (Path): The path to the file to be read.

    Returns:
        str: The content of the file as a single string with newline characters replaced by their literal escape sequences.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def write_string_to_file(string, file_path):
    """
    Writes a given string to a file.

    Args:
        string (str): The string to write.
        file_path (Path): The path to the file where the string will be written.
    """
    with open(file_path, 'w') as file:
        file.write(string)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a configuration file's content to a single-line string.")
    parser.add_argument('--input', required=True, help="Path to the input configuration file.")
    parser.add_argument('--output', required=True, help="Path to the output file where the converted string will be saved.")
    parser.add_argument('--remove-single-quotes', action='store_true', help="Remove all single quote characters from the file content.")

    args = parser.parse_args()

    config_file_path = Path(args.input)
    output_file_path = Path(args.output)
    
    file_content_as_string = read_file_to_string(config_file_path)
    file_content_as_string = file_content_as_string.replace("\r\n", "\\r\\n").replace("\n", "\\n").replace("\r", "\\r")
    
    if args.remove_single_quotes:
        file_content_as_string = file_content_as_string.replace("'", "")
    
    write_string_to_file(file_content_as_string, output_file_path)
    print(f"File content has been converted and saved to: {output_file_path}")
