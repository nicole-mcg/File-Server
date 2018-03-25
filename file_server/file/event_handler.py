from watchdog.events import FileSystemEventHandler

from file_server.packet.impl import FileChangePacket, FileAddPacket, FileDeletePacket, FileMovePacket

class EventHandler(FileSystemEventHandler):
    def __init__(self, packet_queue, directory):
        self.packet_queue = packet_queue
        self.directory = directory

    def on_created(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Created: {}".format(file_name))

        with open(self.directory + file_name, mode='rb') as file:
            file_contents = file.read()
            file.close()
        self.packet_queue.queue_packet(FileAddPacket(
            file_name=file_name,
            file_contents=file_contents
        ))

    def on_deleted(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Deleted: {}".format(file_name))

        self.packet_queue.queue_packet(FileDeletePacket(
            file_name=file_name
        ))

    def on_modified(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Modified: {}".format(file_name))

        with open(self.directory + file_name, mode='rb') as file:
            file_contents = file.read()
            file.close()
        self.packet_queue.queue_packet(FileChangePacket(
            file_name=file_name,
            file_contents=file_contents
        ))

    def on_moved(self, event):
        if (event.is_directory): return False

        file_name = event.src_path[len(self.directory):]
        new_name = event.dest_path[len(self.directory):]

        print("Local File Moved: {}".format(file_name))

        self.packet_queue.queue_packet(FileMovePacket(
            file_name=file_name,
            new_name=new_name
        ))