from InquirerPy import inquirer
import modules.menuActions.menuActions as actions
import modules.types.types as types
from InquirerPy.utils import color_print


def main():
    options = {
        "Add a Telegram User": actions.add_tg_user_action,
        "Delete a Telegram User": lambda: None,
        "Add Spam Messages": lambda: None,
        "Start Spamming": lambda: None,
        "Exit": lambda: None,
    }

    while True:
        action = inquirer.select(
            message="Select an action:",
            choices=options.keys(),
        ).execute()

        if action == "Exit":
            color_print(formatted_text=[("red", "Exited")])
            break

        response: types.Response = options[action]()

        if not response["isSuccess"]:
            color_print(
                formatted_text=[("red", "Error: " + response["error"]["message"])]
            )
        else:
            color_print(formatted_text=[("green", "Done!")])


if __name__ == "__main__":
    main()
