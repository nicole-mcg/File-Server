from watchdog.events import FileSystemEventHandler

from file_server.packet.impl import FileChangePacket, FileAddPacket, FileDeletePacket, FileMovePacket

from time import sleep
from datetime import datetime
from threading import Thread

class FileEvent:

    def __init__(self, packet, time):
        self.packet = packet
        self.time = time


class EventHandler(FileSystemEventHandler):
    def __init__(self, hub_processor, directory):
        self.hub_processor = hub_processor
        self.directory = directory

    def send_file_contents(self, file_name, packet_class, time, count=0):
        try:
            with open(self.directory + file_name, mode='rb') as file:
                pass

            self.hub_processor.queue_packet(FileEvent(
                packet_class(
                    self.hub_processor,
                    file_name=file_name
                ), time)
            )
        except PermissionError:
            # Wait until we can actually read the file
            sleep(500)
            self.send_file_contents(file_name, packet_class, time, count + 1)

    def on_created(self, event):
        if (event.is_directory): return False

        time = datetime.now().microsecond

        file_name = event.src_path[len(self.directory):]

        print("Local File Created: {}".format(file_name))

        Thread(target = self.send_file_contents, args = [file_name, FileAddPacket, time]).start()

    def on_deleted(self, event):
        if (event.is_directory): return False

        time = datetime.now().microsecond

        file_name = event.src_path[len(self.directory):]

        print("Local File Deleted: {}".format(file_name))

        self.hub_processor.queue_packet(FileEvent(
            FileDeletePacket(
                self.hub_processor,
                file_name=file_name
            ), time)
        )

    def on_modified(self, event):
        if (event.is_directory): return False

        time = datetime.now().microsecond

        file_name = event.src_path[len(self.directory):]

        print("Local File Modified: {}".format(file_name))

        Thread(target = self.send_file_contents, args = [file_name, FileChangePacket, time]).start()

    def on_moved(self, event):
        if (event.is_directory): return False

        time = datetime.now().microsecond

        file_name = event.src_path[len(self.directory):]
        new_name = event.dest_path[len(self.directory):]

        print("Local File Moved: {}".format(file_name))

        self.hub_processor.queue_packet(FileEvent(
            FileMovePacket(
                self.hub_processor,
                file_name=file_name,
                new_name=new_name
            ), time)
        )