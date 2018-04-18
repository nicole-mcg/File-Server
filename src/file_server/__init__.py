import sys, builtins, traceback
from threading import Thread, Lock

from file_server.hub.packet_manager import initialize_packet_manager

def start_hub():

    # Check if this is supposed to be a server or client based on number of args entered
    isServer = len(sys.argv) <= 2

    # Get directory to sync
    directory = sys.argv[1]

    # Create the hub
    if isServer:

        from .server import FileServer
        

        # Use FileServer class for hub
        try: 
            hub = FileServer(directory)
        except OSError:
            print("File server could not be started")
            return

    else:

        from .client import FileClient

        # Use FileClient class for hub
        try:
            hub = FileClient(directory, sys.argv[2], sys.argv[3], sys.argv[4])
        except LookupError: # Couldn't authenticate 
            print("Invalid username or password")
            return

    # Add all the packet handlers
    initialize_packet_manager()

    # Starts file watch
    hub.initialize()

    # Runs the hub connection on this thread
    hub.start()

    # Cleanup when the connection has ended
    hub.kill()


def installThreadExcepthook():
    """
    Workaround for sys.excepthook thread bug
    From
http://spyced.blogspot.com/2007/06/workaround-for-sysexcepthook-bug.html
   
(https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    """
    init_old = Thread.__init__
    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run
        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_except_hook
    Thread.__init__ = init

print_lock = Lock()

def exception_hook(*args):
    builtins.print("Error occured in subthread: {}".format(str(traceback.print_last())))
    sys.exit(1)

sys.excepthook = exception_hook

if __name__ == "__main__":

    builtins.old_print = builtins.print

    def new_print(*objects, sep='', end='\n', file=sys.stdout, flush=False):
        print_lock.acquire(True)
        if file is sys.stdout or file is sys.stderr:
            builtins.old_print(*objects, sep=sep, end=end, file=sys.stdout, flush=True)
        else:
            builtins.old_print(*objects, sep=sep, end=end, file=file, flush=flush)
        print_lock.release()

    builtins.print = new_print

    installThreadExcepthook()

    # Make sure args length is correct
    if (len(sys.argv) <= 1):
        print("Command arguments should be in the form \"directory hostname user password\". Only directory is needed for server")
        sys.exit()

    start_hub()