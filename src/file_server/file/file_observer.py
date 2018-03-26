from watchdog.observers import Observer

class FileObserver(Observer):
    def __init__(self, *args):
        Observer.__init__(self, *args)
        self.accepting_events = True
 
    def dispatch_events(self, *args, **kwargs):
        if (len(args[0].queue) > 0):
            with Observer.lock_(self):
                import pdb; pdb.set_trace();
        if (self.accepting_events):
            super(FileObserver, self).dispatch_events(*args, **kwargs)
        else:
            import pdb; pdb.set_trace();