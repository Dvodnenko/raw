import click

from .data import Data


@click.command('tags')
@click.option('--new', default='')
@click.pass_context
def tag(
    ctx: click.Context,
    new: str
):

    if new == '':
        new = []
    else:
        new = new.split(',')

    raww_directory = ctx.obj['raww_directory']
    data = Data(raww_directory)
    mytags = data.tags

    if new:
        for newtag in new:
            if newtag in mytags:
                click.echo(f'🦇 tag {newtag} already exists')
            else:
                data.tags = [*data.tags, newtag]
                click.echo(f'🦇 new tag - {newtag}')
    else:
        if mytags == []:
            click.echo('🦇 your tag list is empty right now')
            exit(1)
        for tag in mytags:
            click.echo(f'* {tag}')
