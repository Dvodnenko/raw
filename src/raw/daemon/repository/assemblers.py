from collections import defaultdict

from ..domain import build_entity


def group_links(rows):
    grouped = defaultdict(list)

    for row in rows:
        from_id = row["from_id"]
        row = dict(row)
        row.pop("from_id")

        grouped[from_id].append(build_entity(**row))

    return grouped

def attach_links(entity_rows, link_rows):
    links_by_entity = group_links(link_rows)

    for row in entity_rows:
        entity = build_entity(**row)
        entity.links = links_by_entity.get(entity.id, [])
        yield entity
