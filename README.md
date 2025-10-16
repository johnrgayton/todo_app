# todo_app

Small command-line to-do app used for learning.

Run the app:

```bash
# from the repository root
python3 -m todo_app.main
```

Run tests:

```bash
# from the repository root
python3 -m unittest discover -s todo_app -p "test_*.py"
```

Utilities

- `todo_app/utils.py` contains `print_items(items, *, title=None, numbered=False, empty_msg=None, bullet="- ")` — a reusable helper that prints iterables in a readable way.

Notes

- `todo_app/__init__.py` is present so the package can be imported (see explanation in README).
