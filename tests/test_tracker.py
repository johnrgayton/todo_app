import os
import tempfile
import sys
import unittest
import json
from pathlib import Path

# Ensure the package root is on sys.path so tests can import todo_app
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))

from todo_app.utils import ActionTracker


class TestActionTracker(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.logpath = os.path.join(self.tmpdir.name, "actions.log")
        self.tracker = ActionTracker(self.logpath)

    def tearDown(self):
        self.tmpdir.cleanup()

    def _read_lines(self):
        with open(self.logpath, "r", encoding="utf8") as f:
            return [json.loads(line) for line in f]

    def test_added_writes_line(self):
        self.tracker.added("Buy milk")
        lines = self._read_lines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["action"], "added")
        self.assertEqual(lines[0]["details"]["item"], "Buy milk")

    def test_deleted_and_edited(self):
        self.tracker.deleted("Old", index=2)
        self.tracker.edited("Old", "New", index=2)
        lines = self._read_lines()
        self.assertEqual(lines[0]["action"], "deleted")
        self.assertEqual(lines[1]["action"], "edited")
        self.assertEqual(lines[1]["details"]["old"], "Old")
        self.assertEqual(lines[1]["details"]["new"], "New")

    def test_listed_records_count(self):
        self.tracker.listed(3)
        lines = self._read_lines()
        self.assertEqual(lines[0]["action"], "listed")
        self.assertEqual(lines[0]["details"]["count"], 3)


if __name__ == "__main__":
    unittest.main()
