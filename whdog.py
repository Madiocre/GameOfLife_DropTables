import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time


class FileChangeHandler(FileSystemEventHandler):
    """
    A handler class that reacts to file system events.
    Specifically, it restarts a script when a Python file is modified.
    """
    def __init__(self, script_path):
        """
        Initializes the handler with the path to the script to be monitored.

        Args:
            script_path (str or Path): The path to the script to be monitored.
        """
        self.script_path = Path(script_path)
        self.process = None
        self.run_script()

    def run_script(self):
        """
        Runs the script in a subprocess. If the script is already running,
        it terminates the existing process before starting a new one.
        """
        if self.process:
            self.process.terminate()
            self.process.wait()  # Wait for the process to fully terminate
        self.process = subprocess.Popen(
            [sys.executable, str(self.script_path)]
            )

    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        Args:
            event (FileSystemEvent): The event representing the file
            system change.
        """
        if Path(event.src_path).suffix == '.py':
            print(f"Detected change in {event.src_path}, restarting...")
            self.run_script()


def watch_directory(script_name, directory='.'):
    """
    Watches a directory for changes to Python files and restarts the specified
    script when a change is detected.

    Args:
        script_name (str): The name of the script to be monitored
        and restarted.
        directory (str): The directory to watch for changes. Defaults to
        the current directory.

    Raises:
        FileNotFoundError: If the specified script is not found
        in the directory.
    """
    script_path = Path(directory) / script_name
    if not script_path.exists():
        raise FileNotFoundError(
            f"Script '{script_name}' not found in '{directory}'"
            )

    event_handler = FileChangeHandler(script_path)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    script_name = "main.py"  # Change this to your script's name
    watch_directory(script_name)
