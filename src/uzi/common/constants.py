from pathlib import Path


## Common data

DAEMON_PID_PATH = Path("/tmp/uzi.pid")
CONFIG_PATH = Path.home() / ".config" / "uzi" / "config.json"
SUPPORTED_SYSTEMS = ("darwin", "linux")
DEFAULT_CONFIG = {
    "core": {
        "db_path": f"{Path.home()}/.uzi.sqlite",
    }
}

## Plist file data (for macOS)

PLIST_LABEL = "com.dvodnenko.uzi"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_LABEL}.plist"

def generate_plist(script_path: Path | str):

    return {
        "Label": PLIST_LABEL,
        "ProgramArguments": [script_path],
        "KeepAlive": {
            "SuccessfulExit": False,
            "Crashed": True,
        },
        "StandardOutPath": "/tmp/uzi.out.log",
        "StandardErrorPath": "/tmp/uzi.err.log",
    }


## Service file data (for Linux)

SERVICE_PATH = Path("/etc") / "systemd" / "system" / "uzi.service"

def generate_service(script_path: Path | str):
    return f"""
[Unit]
Description=uzi Daemon Service
After=network.target

[Service]
ExecStart={script_path}
Restart=on-failure
RestartSec=3
StandardOutput=append:/tmp/uzi.out.log
StandardError=append:/tmp/uzi.err.log

SuccessExitStatus=0
RestartPreventExitStatus=0

[Install]
WantedBy=multi-user.target
    """


## Default values

DEFAULT_FMT = "* {e.title}"
DEFAULT_FSTRING_MARK = "@"
