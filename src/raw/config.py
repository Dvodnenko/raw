import copy
from pathlib import Path
import tomllib


CONFIG_PATH = Path.home() / ".config" / "raw" / "config.toml"
DEFAULT_CONFIG = {
    "core": {
        "database": f"{Path.home()}/.local/share/raw/raw.db",
    },
}


def deep_update(base: dict, updates: dict) -> dict:
    result = copy.deepcopy(base)
    for k, v in updates.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = deep_update(result[k], v)
        else:
            result[k] = v
    return result

def load_raw_config(path: Path):
    with open(path, "rb") as file:
        content = tomllib.load(file)
    return content

config = deep_update(DEFAULT_CONFIG, load_raw_config(CONFIG_PATH))
