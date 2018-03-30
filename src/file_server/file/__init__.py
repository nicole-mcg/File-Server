import sys

from file_server import start_hub

from .file_processor import FileProcessor

def start_file_hub(hub_type, directory):
    start_hub(hub_type, FileProcessor(directory))

if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print("Command arguments should be in the form \"directory hostname user password\". Only directory is needed for server")
        sys.exit()

    directory = sys.argv[1]
    hub_type = "server" if len(sys.argv) <= 2 else "client"

    start_file_hub(hub_type, directory)