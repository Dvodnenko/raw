import inspect
from collections import defaultdict

from ..entities import ENTITIES


def build_entity(**data):
    cls = ENTITIES[data.pop("type")]
    params = inspect.signature(cls).parameters
    return cls(**{k:data.get(k) for k in params})

def group_links(rows):
    grouped = defaultdict(list)

    for row in rows:
        from_id = row["from_id"]
        row = dict(row)
        row.pop("from_id")

        grouped[from_id].append(build_entity(**row))

    return grouped
