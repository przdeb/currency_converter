import json
import logging

from src.config import PROJECT_ROOT

LOG = logging.getLogger(__name__)


def load_json_file(file_name: str, mode: str = "r") -> dict:
    """_summary_

    Args:
        file_name (str): _description_
        mode (str, optional): _description_. Defaults to "r".

    Returns:
        dict: _description_
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
    """_summary_

    Args:
        file_name (str): _description_
        data (dict | list): _description_
        mode (str, optional): _description_. Defaults to "w".

    Raises:
        Exception: _description_
    """
    if not isinstance(data, (dict, list)):
        msg = f"Invalid data format, expected 'dict' or 'list', got {type(data)}"
        LOG.error(msg)
        raise Exception(msg)
    with open(PROJECT_ROOT.joinpath(file_name), mode, encoding="utf-8") as fh:
        json.dump(data, fh, indent=4, default=str)
