import sys
from os import path


def resource_path(relative_path):
    """
    Get the absolute path to a resource, works for both development
    and PyInstaller.

    When running in a development environment, it returns the absolute path
    relative to the current file.
    When running with PyInstaller, it returns the absolute path relative to
    he temporary folder created by PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)
