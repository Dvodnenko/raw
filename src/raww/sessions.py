import time, datetime

import click

from .data import rewrite_data, get_tags, get_active_session, get_sessions, read_data


@click.command('begin')
@click.argument('tags', nargs=-1)
def begin_session(tags: tuple):

    active_session = get_active_session()

    if active_session:
        click.echo('🦇 there is already an active session')
        exit(1)

    if tags == ():
        click.echo('🦇 at least one tag is required to begin a new session')
        exit(1)
    
    mytags = get_tags()
    sessions = get_sessions()

    for tag in tags:
        if tag not in mytags:
            click.echo(f'🦇 tag {tag} does not exist yet')
            exit(1)

    start = datetime.datetime.now()

    new_data = {
        'tags': [*mytags],
        'active_session': {
            'tags': [*tags],
            'start': f'{start}',
            'breaks': 0
        },
        'sessions': [*sessions]
    }

    rewrite_data(new_data)

    click.echo('🦇 session started')
    click.echo()

    if len(tags) == 1:
        click.echo(f'tag - {tags[0]}')
    else:
        click.echo(f'tags: * {tags[0]}')
        for tag in tags[1:]:
            click.echo(f'      * {tag}')

@click.command('finish')
def finish_session():

    active_session = get_active_session()

    if not active_session:
        click.echo('🦇 there is no active session yet')
        exit(1)

    mytags = get_tags()
    mysessions = get_sessions()

    # start & end info
    start_datetime: datetime = datetime.datetime.fromisoformat(active_session.get('start'))
    start_date = datetime.date(start_datetime.year, start_datetime.month, start_datetime.day)
    start_time = datetime.time(start_datetime.hour, start_datetime.minute, start_datetime.second, start_datetime.microsecond)

    end_datetime = datetime.datetime.now()
    end_date = datetime.date(end_datetime.year, end_datetime.month, end_datetime.day)
    end_time = datetime.time(end_datetime.hour, end_datetime.minute, end_datetime.second, end_datetime.microsecond)
    breaks: int = active_session.get('breaks')
    timedelta = ((end_datetime - start_datetime).seconds) - breaks
    hours = timedelta // 3600
    timedelta -= hours*3600
    minutes = timedelta // 60
    timedelta -= minutes * 60
    seconds = timedelta

    tags = [*(active_session.get('tags'))]

    total_time = {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }

    new_session = {
        'tags': [*tags],
        'start': {
            'date': f'{start_date}',
            'time': f'{start_time}'
        },
        'end time': {
            'date': f'{end_date}',
            'time': f'{end_time}'
        },
        'breaks': breaks,
        'total time': total_time
    }

    new_data = {
        'tags': [*mytags],
        'active_session': {},
        'sessions': [*mysessions, new_session]
    }

    rewrite_data(new_data=new_data)

    click.echo('the session has ended 🦇')
    click.echo()
    
    if len(tags) == 1:
        click.echo(f'you did {tags[0]}')
    else:
        click.echo(f'you did: * {tags[0]}')
        for tag in tags[1:]:
            click.echo(f'         * {tag}')

    work_time_info = f'for '
    if hours != 0:
        work_time_info += f'{hours}h '
    if minutes != 0:
        work_time_info += f'{minutes}m '
    work_time_info += f'{seconds}s'

    click.echo(work_time_info)

@click.command('pause')
def pause_session():

    active_session = get_active_session()

    if not active_session:
        click.echo('🦇 there is no active session yet')
        exit(1)

    tags: list = active_session.get('tags')
    breaks: int = active_session.get('breaks')
    data = read_data()

    click.echo('🦇 the session is paused')
    
    while True:
        time.sleep(1)
        breaks += 1

        active_session['breaks'] = breaks
        data['active_session'] = active_session
        rewrite_data(data)
