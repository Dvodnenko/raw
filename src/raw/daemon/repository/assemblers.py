from collections import defaultdict
from typing import Any

from ..database.mappings import COLUMN_TO_TABLE
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

def resolve_tables_to_filter(
    filters: dict[str, tuple[Any]]
):
    table_to_filter_map: dict[str, dict[str, tuple[Any]]] = {}
    for key, value in filters.items():
        if "__" in key: # then it's a complex expression
            table = COLUMN_TO_TABLE[key[0:key.index("__")]]
        else:
            table = COLUMN_TO_TABLE[key]

        if table_to_filter_map.get(table.name):
            table_to_filter_map[table.name].update({key: value})
        else:
            table_to_filter_map[table.name] = {key: value}
    return table_to_filter_map
