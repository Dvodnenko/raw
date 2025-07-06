'''
trying to switch functional aproach to OOP
'''

from pathlib import Path
import pickle, time
from datetime import datetime, date


from .views import format_work_time_info


def create_file_if_not_exists(path: Path, default_content):
    if path.exists():
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    with open(path, 'wb') as file:
        pickle.dump(default_content, file)


class TotalWorkTime:
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @property
    def infostr(self) -> str:
        return format_work_time_info(self.hours, self.minutes, self.seconds)
class Session:
    def __init__(
            self, 
            tags: list[str], 
            start_datetime: datetime, 
            end_datetime: datetime, 
            breaks: int
    ):
        self.tags = tags
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.breaks = breaks

    @property
    def total(self):
        diff = (self.end_datetime - self.start_datetime).seconds - self.breaks

        hours = diff // 3600
        diff -= hours*3600
        minutes = diff // 60
        diff -= minutes * 60
        seconds = diff

        return TotalWorkTime(hours=hours, minutes=minutes, seconds=seconds)
class ActiveSession:
    def __init__(
            self, 
            tags: list[str], 
            start_datetime: datetime,
            breaks: int
    ):
        self.tags = tags
        self.start_datetime = start_datetime
        self.breaks = breaks
    @staticmethod
    def _begin(tags: list, path: Path): # !underhood method!
        active_session = ActiveSession(tags, datetime.now(), 0)
        with open(path, 'wb') as file:
            pickle.dump(active_session, file)
        return active_session
    @staticmethod
    def _finish(path: Path): # !underhood method!
        with open(path, 'rb') as file:
            active_session: ActiveSession = pickle.load(file)
        with open(path, 'wb') as file:
            pickle.dump(None, file)
        return Session(
            active_session.tags, 
            active_session.start_datetime, 
            datetime.now(),
            active_session.breaks
        )
        

class Data:

    __ts_df_title = 'tags.pickle'
    __ss_df_title = 'sessions.pickle'
    __as_df_title = 'active_session.pickle'
    
    def __init__(self, dir: Path):
        self.dir = dir

        self.__tags_path = dir / self.__ts_df_title
        self.__sessions_path = dir / self.__ss_df_title
        self.__as_path = self.dir / self.__as_df_title
    def begin_session(self, tags: list[str]) -> ActiveSession:
        return ActiveSession._begin(tags, path=self.__as_path)
    def finish_session(self) -> Session:
        return ActiveSession._finish(self.__as_path)


    @property
    def tags(self) -> list[str]:
        create_file_if_not_exists(self.__tags_path, [])

        with open(self.__tags_path, 'rb') as file:
            tags: list[str] = pickle.load(file)
        return tags
    @tags.setter
    def tags(self, newtags):
        create_file_if_not_exists(self.__tags_path, [])

        with open(self.__tags_path, 'wb') as file:
            pickle.dump(newtags, file)
        return None

    @property
    def sessions(self) -> list[Session]:
        create_file_if_not_exists(self.__sessions_path, [])

        with open(self.__sessions_path, 'rb') as file:
            sessions: list[str] = pickle.load(file)
        return sessions
    @sessions.setter
    def sessions(self, newsessions):
        create_file_if_not_exists(self.__sessions_path, [])

        with open(self.__sessions_path, 'wb') as file:
            pickle.dump(newsessions, file)
        return None

    @property
    def active_session(self) -> ActiveSession | None:
        create_file_if_not_exists(self.__as_path, None)

        with open(self.__as_path, 'rb') as file:
            active_session: ActiveSession | None = pickle.load(file)
        return active_session
    @active_session.setter
    def active_session(self, activesession):
        create_file_if_not_exists(self.__as_path, None)

        with open(self.__as_path, 'wb') as file:
            pickle.dump(activesession, file)
        return None


DIR_PATH = Path.home() / 'Dev' / 'raww' / 'src' / 'tests' # test path

data = Data(DIR_PATH)
