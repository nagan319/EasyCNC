from watchdog.events import FileSystemEventHandler

class TestEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.modified_files = []

    def on_modified(self, event):
        if not event.is_directory:
            self.modified_files.append(event.src_path)
            print(f'File modified during test: {event.src_path}')
            