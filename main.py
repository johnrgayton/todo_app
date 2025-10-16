from todo_app import print_items

commands_list = ["add", "list", "edit", "delete", "exit"]
cmd_ls_str = ", ".join(commands_list)

todos = []


while True:
    command = input(f"Enter a command ({cmd_ls_str}): ").strip().lower()

    if command == "add":
        todo = input("Enter a new to-do item: ").strip()
        todos.append(todo)
        print(f'Added: "{todo}"')

    elif command == "list":
        print_items(todos, title="To-do items:", numbered=True, empty_msg="No to-do items.")

    elif command == "edit":
        if not todos:
            print("No to-do items to edit.")
            continue
        try:
            print_items(todos, title="To-do items:", numbered=True, empty_msg="No to-do items.")
            index = int(input("Enter the number of the to-do item to edit: ")) - 1
            if 0 <= index < len(todos):
                new_text = input("Enter the new text: ").strip()
                old = todos[index]
                todos[index] = new_text
                print(f'Updated: "{old}" -> "{new_text}"')
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")

    elif command == "delete":
        if not todos:
            print("No to-do items to delete.")
            continue
        try:
            index = int(input("Enter the number of the to-do item to delete: ")) - 1
            if 0 <= index < len(todos):
                removed = todos.pop(index)
                print(f'Deleted: "{removed}"')
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")

    elif command == "exit":
        print("Exiting the to-do app.")
        break

    else:
        print("Unknown command. Please use add, list, delete, or exit.")