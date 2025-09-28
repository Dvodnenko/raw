import os

import click

from ...domain import Group, Color, EntityType
from ...application import GroupService
from ...infrastructure import PickleGroupRepository


@click.command("create")
@click.argument("path")
@click.option("--icon", default="")
@click.option("--color", 
              type=click.Choice([c.value for c in Color], case_sensitive=False), 
              default=Color.WHITE)
@click.pass_context
def groups_create(ctx: click.Context, path: str, icon: str, color: str):
    picked_color_from_enum = Color._member_map_.get(color.upper(), Color.WHITE)
    service = GroupService(repo=PickleGroupRepository(), config=ctx.obj)
    group = Group(path, type=EntityType.GROUP, refs=[], color=picked_color_from_enum, icon=icon)
    ucr = service.create(group=group)
    click.echo(f"raw: {ucr.message}")
    exit(ucr.status_code)


@click.command("update")
@click.argument("path")
@click.option("--path", "new_path", default="")
@click.option("--icon", default="")
@click.option("--color", 
              type=click.Choice([c.value for c in Color], case_sensitive=False), 
              default=Color.WHITE)
@click.pass_context
def groups_update(ctx: click.Context, path: str, new_path: str, icon: str, color: str):
    picked_color_from_enum = Color._member_map_.get(color.upper(), Color.WHITE)
    service = GroupService(repo=PickleGroupRepository(), config=ctx.obj)
    new_group = Group(subpath=new_path if new_path!="" else path, 
                      type=EntityType.GROUP, 
                      refs=[], 
                      color=picked_color_from_enum, icon=icon)
    ucr = service.update(path, new=new_group)
    click.echo(f"raw: {ucr.message}")
    exit(ucr.status_code)


@click.command("delete")
@click.argument("path")
@click.pass_context
def groups_delete(ctx: click.Context, path: str):
    if os.geteuid() != 0:
        click.echo("raw: This command must be run as root")
        exit(5)
    service = GroupService(repo=PickleGroupRepository(), config=ctx.obj)
    ucr = service.delete(path)
    click.echo(f"raw: {ucr.message}")
    exit(ucr.status_code)
