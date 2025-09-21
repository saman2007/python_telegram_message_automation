from InquirerPy import inquirer
from InquirerPy.base.control import Choice


def main():
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Add a Telegram User",
            "Delete a Telegram User",
            "Add Spam Messages",
            "Start Spamming",
            "Exit",
        ],
    ).execute()


if __name__ == "__main__":
    main()
