import click

from .connection import request
from .parser import parse_cli_args


class ProxyGroup(click.Group):
    def resolve_command(self, ctx, args):
        if args[0] in self.commands:
            cmd_name, cmd, args = super().resolve_command(ctx, args)
            return cmd_name, cmd, args
        args_, kwargs, flags = parse_cli_args(args)
        response = request(args_, kwargs, flags)
        click.echo(response)
        exit(0)
