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
