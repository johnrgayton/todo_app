import io
import sys
import unittest
from pathlib import Path

# Ensure the package root is on sys.path so tests can import todo_app
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))

from todo_app.utils import print_items


class TestPrintItems(unittest.TestCase):
    def capture(self, func, *args, **kwargs):
        buf = io.StringIO()
        old = sys.stdout
        try:
            sys.stdout = buf
            func(*args, **kwargs)
            return buf.getvalue()
        finally:
            sys.stdout = old

    def test_empty_iterable(self):
        out = self.capture(print_items, [], title="Items:", numbered=True, empty_msg="No items.")
        self.assertIn("No items.", out)

    def test_string_treated_as_single_item(self):
        out = self.capture(print_items, "hello", title="Greeting:", numbered=False, empty_msg="No items.")
        self.assertIn("Greeting:", out)
        self.assertIn("- hello", out)

    def test_numbered_output(self):
        out = self.capture(print_items, ["a", "b"], title="List:", numbered=True)
        self.assertIn("1. a", out)
        self.assertIn("2. b", out)

    def test_custom_bullet(self):
        out = self.capture(print_items, ["x"], title=None, numbered=False, bullet="* ")
        self.assertIn("* x", out)


if __name__ == "__main__":
    unittest.main()
