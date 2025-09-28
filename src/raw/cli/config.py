from pathlib import Path
import json

from ..domain import Config, CoreSettings


CONFIG_FILE_PATH = Path.home() / ".config" / "raw" / "config.json"


def load_config() -> Config:
    with open(CONFIG_FILE_PATH, "r") as file:
        data: dict = json.load(file)

    core = CoreSettings(rootgroup=Path(data.get("rootgroup")))
    config = Config(core=core)
    return config
