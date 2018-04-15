import time
from threading import Thread

from watchdog.events import FileSystemEventHandler

from file_server.hub.packets.file_change import FileChangePacket
from file_server.hub.packets.file_add import FileAddPacket
from file_server.hub.packets.file_delete import FileDeletePacket
from file_server.hub.packets.file_move import FileMovePacket

# This class is used to handle events from the file watch
class FileEventHandler(FileSystemEventHandler):

    # FIXME this should be move into an instance of FileEventHandler to be consistent with add_ignore and pop_ignore methods
    # The dictionary of events to ignore
    # key: See comments for add_ignore
    # value: An integer representing the number of times to ignore this event
    events_to_ignore = {}

    # hub: the hub that the file watch is associated with
    # directory: the directory that is being watched
    def __init__(self, hub, directory):
        self.hub = hub
        self.directory = directory

    # Adds an event to be ignored once
    # data: A tuple containing a string for the type of event and the file path from the root directory. E.g ("change", path)
    def add_ignore(self, data):

        # Adds ignore or increments by 1 if it exists
        if data in FileEventHandler.events_to_ignore:
            FileEventHandler.events_to_ignore[data] += 1
        else:
            FileEventHandler.events_to_ignore[data] = 1

    # Checks if an event should be ignored
    # Decrements the number of times to ignore the event (this method "uses" an ignore)
    def pop_ignore(self, data):

        # Check if the ignore exists
        if not data in FileEventHandler.events_to_ignore:

            # Don't ignore the event
            return False

        else:

            # Remove the ignore or decrement it by 1
            if FileEventHandler.events_to_ignore[data] == 1:
                del FileEventHandler.events_to_ignore[data]
            else:
                FileEventHandler.events_to_ignore[data] -= 1

        # This event should be ignored
        return True

    # Queues a file change packet
    # Waits until the file is allowed to be accessed
    def send_file_contents(self, file_name, packet_class, data, num_attempts=0):

        try:

            # Try to open the file
            with open(self.directory + file_name, mode='rb') as file:
                pass

        except PermissionError:
            # The file can't be accessed at the moment so wait 500ms
            time.sleep(0.5)

            # Try again
            self.send_file_contents(file_name, packet_class, data, num_attempts + 1)

            return

        # We were able to open the file, so let's queue the packet
        self.hub.queue_packet(
            packet_class(
                self.hub,
                file_name=file_name
            ), data
        )

    # Called when a local file is created
    def on_created(self, event):

        # FIXME directories are not currently handled
        if (event.is_directory): 
            print("Created directory: " + str(event.src_path))
            return False

        # Get the path of the file changed (from the root watch directory)
        file_name = event.src_path[len(self.directory):]

        print("Local File Modified: {}".format(file_name))

        # Event ignore data
        data = ("change", file_name)

        # Check if this event should be ignored
        if not self.pop_ignore(data):

            # Queue the FileAddPacket when the file is allowed to be opened
            Thread(target = self.send_file_contents, args = [file_name, FileAddPacket, data]).start()

    # Called when a local file is modified
    # This can be called when a file is created (on top of on_created)
    def on_modified(self, event):

        # FIXME directories are not currently handled
        if (event.is_directory): 
            print("Modified directory: " + str(event.src_path))
            return False

        # Get the path of the file changed (from the root watch directory)
        file_name = event.src_path[len(self.directory):]

        print("Local File Modified: {}".format(file_name))

        # Event ignore data
        data = ("change", file_name)

        # Check if this event should be ignored
        if not self.pop_ignore(data):

            # Queue the FileChangePacket when the file is allowed to be opened
            Thread(target = self.send_file_contents, args = [file_name, FileChangePacket, data]).start()

    # Called when a local file is deleted
    def on_deleted(self, event):

        # FIXME directories are not currently handled
        if (event.is_directory): 
            print("Deleted directory: " + str(event.src_path))
            return False

        # Get the path of the file changed (from the root directory)
        file_name = event.src_path[len(self.directory):]

        print("Local File Deleted: {}".format(file_name))

        # Event ignore data
        data = ("delete", file_name)

        # Queue the packet if this event shouldn't be ignored
        if not self.pop_ignore(data):
            self.hub.queue_packet(
                FileDeletePacket(
                    self.hub,
                    file_name=file_name
                ), data
            )

    # Called when a local file is moved
    def on_moved(self, event):

        # FIXME directories are not currently handled
        if (event.is_directory): 
            print("Moved directory: " + str(event.src_path))
            return False

        # Get the old file path (from the root directory)
        file_name = event.src_path[len(self.directory):]

        # Get the new file path (from the root directory)
        new_name = event.dest_path[len(self.directory):]

        print("Local File Moved: {}".format(file_name))

        # Event ignore data
        data = ("move", file_name, new_name)

        # Queue the packet if this event shouldn't be ignored
        if not self.pop_ignore(data):
            self.hub.queue_packet(
                FileMovePacket(
                    self.hub,
                    file_name=file_name,
                    new_name=new_name
                ), data
            )