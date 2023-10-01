import json
import logging

from src.config import PROJECT_ROOT

LOG = logging.getLogger(__name__)


def load_json_file(file_name: str, mode: str = "r") -> dict:
    """Function to read JSON file and return its content.

    Args:
        file_name (str): Relative path to a file (from project root)
        mode (str, optional): Mode to open JSON file. Defaults to "r".

    Returns:
        dict: File content.
    """
    file_name = PROJECT_ROOT.joinpath(file_name)
    try:
        with open(file_name, mode, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError:
        LOG.error(f"Failed to read file {file_name}")
        raise
    except FileNotFoundError:
        LOG.error(f"File {file_name} does not exist")
        raise


def save_json_file(file_name: str, data: dict | list, mode: str = "w"):
    """Function to save data in a JSON file.

    Args:
        file_name (str): Relative path to a file (from project root)
        data (dict | list): Data to be saved in a file.
        mode (str, optional): Mode to open JSON file. Defaults to "w".

    Raises:
        Exception: When data is in invalid format.
    """
    if not isinstance(data, (dict, list)):
        msg = f"Invalid data format, expected 'dict' or 'list', got {type(data)}"
        LOG.error(msg)
        raise Exception(msg)
    with open(PROJECT_ROOT.joinpath(file_name), mode, encoding="utf-8") as fh:
        json.dump(data, fh, indent=4, default=str)
