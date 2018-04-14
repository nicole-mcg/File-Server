import time
from threading import Thread

from watchdog.events import FileSystemEventHandler

from file_server.packet.impl import FileChangePacket, FileAddPacket, FileDeletePacket, FileMovePacket

class FileEventHandler(FileSystemEventHandler):

    events_to_ignore = {}

    def add_ignore(self, data):
        if data in FileEventHandler.events_to_ignore:
            FileEventHandler.events_to_ignore[data] += 1
        else:
            FileEventHandler.events_to_ignore[data] = 1

    def __init__(self, hub, directory):
        self.hub = hub
        self.directory = directory

    def send_file_contents(self, file_name, packet_class, data, count=0):
        try:
            with open(self.directory + file_name, mode='rb') as file:
                pass

            self.hub.queue_packet(
                packet_class(
                    self.hub,
                    file_name=file_name
                ), data
            )
        except PermissionError:
            # Wait until we can actually read the file
            time.sleep(500)
            self.send_file_contents(file_name, packet_class, data, count + 1)

    def check_ignore(self, data):
        if not data in FileEventHandler.events_to_ignore:
            return False
        else:
            if FileEventHandler.events_to_ignore[data] == 1:
                del FileEventHandler.events_to_ignore[data]
            else:
                FileEventHandler.events_to_ignore[data] -= 1
        return True

    def on_created(self, event):
        if (event.is_directory): 
            print("Created directory: " + str(event.src_path))
            return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Modified: {}".format(file_name))

        data = ("change", file_name)

        if not self.check_ignore(data):
            Thread(target = self.send_file_contents, args = [file_name, FileAddPacket, data]).start()

    def on_modified(self, event):
        if (event.is_directory): 
            print("Modified directory: " + str(event.src_path))
            return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Modified: {}".format(file_name))

        data = ("change", file_name)

        if not self.check_ignore(data):
            Thread(target = self.send_file_contents, args = [file_name, FileChangePacket, data]).start()

    def on_deleted(self, event):
        if (event.is_directory): 
            print("Deleted directory: " + str(event.src_path))
            return False

        file_name = event.src_path[len(self.directory):]

        print("Local File Deleted: {}".format(file_name))

        data = ("delete", file_name)

        if not self.check_ignore(data):
            self.hub.queue_packet(
                FileDeletePacket(
                    self.hub,
                    file_name=file_name
                ), data
            )

    def on_moved(self, event):
        if (event.is_directory): 
            print("Moved directory: " + str(event.src_path))
            return False

        file_name = event.src_path[len(self.directory):]
        new_name = event.dest_path[len(self.directory):]

        print("Local File Moved: {}".format(file_name))

        data = ("move", file_name, new_name)

        if not self.check_ignore(data):
            self.hub.queue_packet(
                FileMovePacket(
                    self.hub,
                    file_name=file_name,
                    new_name=new_name
                ), data
            )