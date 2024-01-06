import os
import json
import sys

from src.constants.constants import LDPLAYER_PATH


def open_file(filename, folder):
    # Get the full path to the file
    path = os.path.join(os.path.expanduser('~'), folder, filename)
    # Open the file and read its contents
    with open(path, 'r') as f:
        contents = json.load(f)
    # Return the contents of the file
    return contents


def save_json_file(data, filename, folder):
    path = os.path.join(os.path.expanduser('~'), folder, filename)
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


def rename_txt_files(directory, index):
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                old_path = os.path.join(directory, filename)
                new_filename = "new_" + filename
                new_path = os.path.join(directory, new_filename)

                os.rename(old_path, new_path)
                print(f"File '{filename}' renamed to '{new_filename}' successfully.")
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
    except FileExistsError:
        print(f"Error: File 'ledian{index}' already exists.")


def rename_folder(old_name, new_name):
    try:
        os.rename(old_name, new_name)
    except FileNotFoundError:
        print(f"Error: Folder '{old_name}' not found.")
    except FileExistsError:
        print(f"Error: Folder '{new_name}' already exists.")




