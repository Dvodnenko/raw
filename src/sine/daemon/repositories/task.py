from sqlalchemy import select
from sqlalchemy.orm import Session as ormSession

from ..entities import Task


class saTaskRepository:
    def __init__(self, session: ormSession):
        self.session = session

    def create(self, task: Task):
        self.session.add(task)
        self.session.commit()
        yield

    def get(self, title: str):
        query = select(Task) \
            .where(Task.title == title)
        obj = self.session.scalars(query).first()
        yield obj

    def get_all(self, order_by: str = "title"):
        batch_size = 100
        offset = 0
        while True:
            batch = self.session.query(Task).order_by(getattr(Task, order_by)).\
                limit(batch_size).offset(offset).all()
            if not batch:
                break
            for obj in batch:
                yield obj
            offset += batch_size

    def update(self, title_: str, **kwargs):
        task = (self.session.query(Task)
                  .filter_by(title=title_)
                  .first())
        task = task.update(**kwargs)
        self.session.commit()
        yield

    def delete(self, entity: Task):
        self.session.delete(entity)
        self.session.commit()
        yield
