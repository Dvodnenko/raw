import inspect

from ..entities import ENTITIES


def build_entity(**data):
    cls = ENTITIES[data.pop("type")]
    params = inspect.signature(cls).parameters
    return cls(**{k:data.get(k) for k in params})
