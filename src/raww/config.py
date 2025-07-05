import json
from pathlib import Path


CONFIG_DIR = Path.home() / '.config' / 'raww'
CONFIG_FILE = CONFIG_DIR / 'config.json'
DEFAULT_RAWW_DIR = Path.home() / '.raww'
DEFAULT_RAWW_DF = DEFAULT_RAWW_DIR / 'data.json' # DF stands for data file


def load_config():
    if not CONFIG_FILE.exists():
        return {'raww_datafile': str(DEFAULT_RAWW_DF)}
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)
    
def save_config(config: dict): 
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)
