from watchdog.events import FileSystemEventHandler

from file_server.packet.impl import FileChangePacket, FileAddPacket, FileDeletePacket, FileMovePacket

from time import sleep

class EventHandler(FileSystemEventHandler):
    def __init__(self, hub_processor, directory):
        self.hub_processor = hub_processor
        self.directory = directory

    def get_file_contents(self, file_name, count=0):
        try:
            with open(self.directory + file_name, mode='rb') as file:
                file_contents = file.read()
        except PermissionError:
            sleep(50)
            file_contents = self.get_file_contents(file_name, count + 1)
            if (count > 5):
                import pdb;pdb.set_trace();

        return file_contents

    def on_created(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Created: {}".format(file_name))

        file_contents = self.get_file_contents(file_name)

        self.hub_processor.queue_packet(FileAddPacket(
            file_name=file_name,
            file_contents=file_contents
        ))

    def on_deleted(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Deleted: {}".format(file_name))

        self.hub_processor.queue_packet(FileDeletePacket(
            file_name=file_name
        ))

    def on_modified(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Modified: {}".format(file_name))

        file_contents = self.get_file_contents(file_name)

        self.hub_processor.queue_packet(FileChangePacket(
            file_name=file_name,
            file_contents=file_contents
        ))

    def on_moved(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]
        new_name = event.dest_path[len(self.directory):]

        print("Local File Moved: {}".format(file_name))

        self.hub_processor.queue_packet(FileMovePacket(
            file_name=file_name,
            new_name=new_name
        ))