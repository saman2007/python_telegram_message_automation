from InquirerPy import inquirer
import modules.menuActions.menuActions as actions
import modules.types.types as types
from InquirerPy.utils import color_print
from modules.helpers.helpers import initialize
from modules.static.constants import GITHUB_ADDRESS

NOT_IMPLEMENTED_OPTION_ERROR: types.Response = {
    "error": {"message": "Option is not implemented yet, coming soon!", "code": 503},
    "isSuccess": False,
}


def main():
    try:
        initialize()
    except Exception as e:
        color_print(
            formatted_text=[
                (
                    "red",
                    "An error occurred during the initialization of the app.\nThe exact error message is:\n",
                ),
                ("white", str(e)),
                ("white", "\n"),
                (
                    "red",
                    f"If you think there is anything wrong with the code, feel free to open an issue on the project’s GitHub.\n Github: {GITHUB_ADDRESS} \nExited.",
                ),
            ]
        )

        return

    options = {
        "Add a Telegram User": actions.add_tg_user_action,
        "Show Telegram Users": actions.show_tg_users_action,
        "Delete a Telegram User": actions.delete_tg_user_action,
        "Add a Spam Message": actions.add_spam_messages_action,
        "Show Spam Messages": actions.show_spam_messages_action,
        "Start Spamming": actions.start_spamming_action,
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
                formatted_text=[
                    ("red", "Error: " + response["error"]["message"]),
                    ("white", "\n"),
                    (
                        "red",
                        "If you think there is anything wrong with the code, feel free to open an issue on the project’s GitHub which you can find in Github option in the menu.",
                    ),
                ]
            )
        else:
            color_print(formatted_text=[("green", "Done!")])


if __name__ == "__main__":
    main()
