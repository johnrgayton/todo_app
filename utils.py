def print_items(items, *, title=None, numbered=False, empty_msg=None, bullet="- "):
    """Print an iterable's items in a readable way.

    Parameters:
      items: any iterable (lists, tuples, generators). Strings are treated as a single item.
      title: optional header to print before the items.
      numbered: if True, prefix lines with a 1-based index.
      empty_msg: message to print when the iterable is empty. If None, prints nothing.
      bullet: prefix for each line when not numbered.

    This helper is intentionally generic and not tied to the variable name `todos`.
    Example:
      print_items(my_list, title="Items:", numbered=True, empty_msg="No items.")
    """
    # Handle strings specially: treat a string as a single item, not an iterable of chars
    if isinstance(items, (str, bytes)):
        items_list = [items]
    else:
        try:
            # Materialize to allow multiple passes (enumerate, len checks)
            items_list = list(items)
        except TypeError:
            # Not iterable
            if empty_msg:
                print(empty_msg)
            return

    if not items_list:
        if empty_msg:
            print(empty_msg)
        return

    if title:
        print(title)

    if numbered:
        for i, it in enumerate(items_list, start=1):
            print(f"{i}. {it}")
    else:
        for it in items_list:
            print(f"{bullet}{it}" if bullet else f"{it}")


import json
from datetime import datetime
from pathlib import Path


class ActionTracker:
    """Record user actions to a JSON Lines file.

    Each line is a JSON object with at minimum:
      - timestamp: ISO 8601
      - action: string (added, edited, deleted, listed, etc.)
      - details: dict with action-specific keys

    The log file defaults to a file named `actions.log` next to this module.

    For tests, pass a temporary path.
    """

    def __init__(self, path: str | Path | None = None):
        if path is None:
            self.path = Path(__file__).resolve().parent / "actions.log"
        else:
            self.path = Path(path)

        # Ensure parent exists
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            # Best-effort: omit creating if not allowed
            pass

    def _now(self) -> str:
        return datetime.utcnow().isoformat() + "Z"

    def _write(self, record: dict) -> None:
        record.setdefault("timestamp", self._now())
        # Write a JSON line
        with open(self.path, "a", encoding="utf8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def record(self, action: str, details: dict | None = None) -> None:
        payload = {"action": action, "details": details or {}}
        self._write(payload)

    # convenience helpers
    def added(self, item: str) -> None:
        self.record("added", {"item": item})

    def edited(self, old: str, new: str, index: int | None = None) -> None:
        d = {"old": old, "new": new}
        if index is not None:
            d["index"] = index
        self.record("edited", d)

    def deleted(self, item: str, index: int | None = None) -> None:
        d = {"item": item}
        if index is not None:
            d["index"] = index
        self.record("deleted", d)

    def listed(self, count: int | None = None) -> None:
        d = {}
        if count is not None:
            d["count"] = count
        self.record("listed", d)
