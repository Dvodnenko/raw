import sys

from ..icmds import (
    daemon_start_darwin, daemon_stop_darwin, init_darwin, daemon_restart_darwin,
    daemon_start_linux, daemon_stop_linux, init_linux, daemon_restart_linux,
    daemon_disable_linux, daemon_enable_linux, daemon_load_darwin, daemon_remove_darwin,
    daemon_unload_darwin,
)


if sys.platform.lower() == "darwin":
    INTERNAL_CMD_MAP = {
        "init": init_darwin,
        "daemon": {
            "start": daemon_start_darwin,
            "stop": daemon_stop_darwin,
            "restart": daemon_restart_darwin,
            "load": daemon_load_darwin,
            "unload": daemon_unload_darwin,
            "remove": daemon_remove_darwin,
        },
    }
elif sys.platform.lower() == "linux":
    INTERNAL_CMD_MAP = {
        "init": init_linux,
        "daemon": {
            "start": daemon_start_linux,
            "stop": daemon_stop_linux,
            "restart": daemon_restart_linux,
            "enable": daemon_enable_linux,
            "disable": daemon_disable_linux,
        },
    }
