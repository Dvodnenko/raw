from typing import Optional


def _extract_parent_title(full_path: str) -> Optional[str]:
        if full_path.count("/") == 1: # root entity
            return None
        return full_path[0:full_path.rfind("/")]
