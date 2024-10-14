# import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.run_script()

    def run_script(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}, restarting...")
            self.run_script()


if __name__ == "__main__":
    script_name = "main.py"  # Change this to your script's name
    event_handler = FileChangeHandler(script_name)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
