import json

import click

from ..config import load_config
from .commands.daemon import daemon_start, daemon_stop
from .constants import DEFAULT_CONFIG, CONFIG_PATH
from .proxy import ProxyGroup


__version__ = "1.3.4"

@click.group(cls=ProxyGroup)
@click.version_option(package_name="raw")
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()

    ctx.obj = config


@click.command("init")
@click.option("-force", is_flag=True)
def raw_init(force):
    exist = CONFIG_PATH.exists()
    if not exist:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.touch(exist_ok=True)
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        exit(0)
    elif force:
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        exit(0)
    click.echo("raw: you already have a non-deafault config file")
    exit(1)

## Core Commands
raw.add_command(raw_init)

## Daemon Commands

@raw.group
def daemon(): ...

daemon.add_command(daemon_start)
daemon.add_command(daemon_stop)
