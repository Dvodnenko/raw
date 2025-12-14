import shutil
import json

from ....common.constants import CONFIG_PATH, DEFAULT_CONFIG, generate_service, SERVICE_PATH
from ....common import load_config


def init(rspd):
    _, flags, _ = rspd["ps"]["afk"]
    
    ## Config

    force = "F" in flags

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.touch(exist_ok=True)
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
    elif force:
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
    else:
        yield "You already have a non-default config file", 1
        

    ## Service file (for Linux)

    # can't use common.config.config_ here because it could be 
    # changed above, so i re-run the method
    config = load_config()
    service_content = generate_service(config.get("daemon_bin_path", 
                                              shutil.which("rawd")))
    if not SERVICE_PATH.exists():
        SERVICE_PATH.parent.mkdir(parents=True, exist_ok=True)
        SERVICE_PATH.touch(exist_ok=True)
        with open(SERVICE_PATH, "w") as file:
            file.write(service_content)
        return
    elif force:
        with open(SERVICE_PATH, "w") as file:
            file.write(service_content)
        return
    else:
        yield "You already have a non-default service file", 1
