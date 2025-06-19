def format_work_time_info(
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0
) -> str:

    if hours == 0 and minutes == 0 and seconds == 0:
        return '0s'
    
    work_time_info = ''

    if hours != 0:
        work_time_info += f'{hours}h '
    if minutes != 0:
        work_time_info += f'{minutes}m '
    if seconds != 0:
        work_time_info += f'{seconds}s'

    return work_time_info
