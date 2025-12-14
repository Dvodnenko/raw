from pathlib import Path


## Common data

DAEMON_PID_PATH = Path("/tmp/raw.pid")
CONFIG_PATH = Path.home() / ".config" / "raw" / "config.json"
SUPPORTED_SYSTEMS = ("darwin", "linux")
DEFAULT_CONFIG = {
    "core": {
        "db_path": f"{Path.home()}/.raw.sqlite",
    }
}

## Plist file data (for macOS)

PLIST_LABEL = "com.dvodnenko.raw"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_LABEL}.plist"

def generate_plist(script_path: Path | str):

    return {
        "Label": PLIST_LABEL,
        "ProgramArguments": [script_path],
        "KeepAlive": {
            "SuccessfulExit": False,
            "Crashed": True,
        },
        "StandardOutPath": "/tmp/raw.out.log",
        "StandardErrorPath": "/tmp/raw.err.log",
    }


## Service file data (for Linux)

SERVICE_PATH = Path("/etc") / "systemd" / "system" / "raw.service"

def generate_service(script_path: Path | str):
    return f"""
[Unit]
Description=raw Daemon Service
After=network.target

[Service]
ExecStart={script_path}
Restart=on-failure
RestartSec=3
StandardOutput=append:/tmp/raw.out.log
StandardError=append:/tmp/raw.err.log

SuccessExitStatus=0
RestartPreventExitStatus=0

[Install]
WantedBy=multi-user.target
    """


## Default values

DEFAULT_FMT = "* {e.title}"
DEFAULT_FSTRING_MARK = "@"
