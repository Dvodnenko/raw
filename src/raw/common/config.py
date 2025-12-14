from pathlib import Path
import json


CONFIG_FILE_PATH = Path.home() / ".config" / "raw" / "config.json"
CONFIG_GLOBALS = {}


def load_config() -> dict:
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            data: dict = json.load(file)

        return data
    except FileNotFoundError as _:
        return {}

config_ = load_config()

def exe_lines(
    lines: list,
    globals: dict,
):
    if not lines:
        return
    for line in lines:
        exec(line, globals=globals)
