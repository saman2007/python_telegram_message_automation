from InquirerPy import inquirer
import modules.helpers.helpers as helpers
import json
import asyncio
import modules.types.types as types
from InquirerPy.utils import color_print
from modules.static.constants import STORED_TG_USERS, STORED_TG_SPAM_MESSAGES
import typing


def add_tg_user_action() -> types.Response:
    api_id = inquirer.text("Enter your api id: ").execute()
    api_hash = inquirer.text("Enter your api hash: ").execute()
    phone_number = inquirer.text(
        "Enter your phone number(with international form): "
    ).execute()

    try:
        if not helpers.looks_international(phone_number):
            raise Exception(
                "Enter your phone number in international format like this:\n+989171111111"
            )

        if helpers.is_user_exist(phone_number):
            raise Exception("This account already exists.")

        user_info = asyncio.run(
            helpers.get_tg_user_info(int(api_id), api_hash, phone_number)
        )

        if not user_info:
            raise Exception("No info found.")

        with open(STORED_TG_USERS, "r+", encoding="utf-8") as f:
            accounts: typing.Dict[str, types.Account] = json.loads(f.read())

            if f"@{user_info.username}" in accounts:
                raise Exception("This account already exists.")

            accounts[f"@{user_info.username}"] = {
                "api_id": int(api_id),
                "api_hash": api_hash,
                "phone_number": phone_number,
            }

            proceed = inquirer.confirm(
                message=f"Accounts username is @{user_info.username}. Is it OK to continue?",
                default=True,
            ).execute()

            if not proceed:
                raise Exception("Operation aborted.")

            f.seek(0)
            f.write(json.dumps(accounts))
            f.truncate()

            return {
                "error": None,
                "isSuccess": True,
            }

    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}


def show_tg_users_action() -> types.Response:
    try:
        with open(STORED_TG_USERS, "r", encoding="utf-8") as f:
            accounts: typing.Dict[str, types.Account] = json.loads(f.read())

            if len(accounts.keys()) > 0:
                color_print(formatted_text=[("purple", f"___________")])

            for username in accounts:
                color_print(
                    formatted_text=[
                        ("white", "Username: "),
                        ("orange", f"{username}\n"),
                        ("white", "API ID: "),
                        ("orange", f"{accounts[username]["api_id"]}\n"),
                        ("white", "API Hash: "),
                        ("orange", f"{accounts[username]["api_hash"]}\n"),
                        ("white", "Phone Number: "),
                        ("orange", f"{accounts[username]["phone_number"]}\n"),
                        ("purple", f"___________"),
                    ]
                )

            return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"message": str(e), "code": 500}, "isSuccess": False}


def delete_tg_user_action() -> types.Response:
    try:
        with open(STORED_TG_USERS, "r", encoding="utf-8") as f:
            accounts: typing.Dict[str, types.Account] = json.loads(f.read())

        selected_username = inquirer.select(
            message="Select the user that you want to delete:",
            choices=accounts.keys(),
        ).execute()

        account = accounts[selected_username]

        is_logged_out = asyncio.run(
            helpers.log_out_user(
                account["api_id"], account["api_hash"], account["phone_number"]
            )
        )

        if not is_logged_out:
            raise Exception(
                "Couldn't log out from your account. Please check your internet or try again later."
            )

        del accounts[selected_username]

        with open(STORED_TG_USERS, "w") as f:
            f.write(json.dumps(accounts))
            f.truncate()

        return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}


def add_spam_messages_action() -> types.Response:
    spam_message = inquirer.text("Enter your spam message: ").execute()
    try:
        with open(STORED_TG_SPAM_MESSAGES, "r+", encoding="utf-8") as f:
            spam_messages = json.loads(f.read())
            print(spam_message)
            spam_messages.append(spam_message)
            f.seek(0)
            f.write(json.dumps(spam_messages))
            f.truncate()

            return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}


def show_spam_messages_action() -> types.Response:
    try:
        with open(STORED_TG_SPAM_MESSAGES, "r", encoding="utf-8") as f:
            spam_messages = json.loads(f.read())

            if len(spam_messages) > 0:
                color_print(formatted_text=[("purple", f"___________")])

            for spam_message in spam_messages:
                color_print(
                    formatted_text=[
                        ("orange", spam_message + "\n"),
                        ("purple", "___________"),
                    ]
                )

            return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}


def start_spamming_action() -> types.Response:
    try:
        with open(STORED_TG_USERS, "r", encoding="utf-8") as f:
            accounts: typing.Dict[str, types.Account] = json.loads(f.read())

        if len(accounts.keys()) == 0:
            raise Exception(
                "You must add least add one account to the list of accounts which is possible by selecting 'Add a Telegram User' option."
            )

        selected_accounts = inquirer.checkbox(
            "Select the accounts that you want to spam with:",
            accounts.keys(),
            validate=lambda result: len(result) >= 1,
            invalid_message="Must be at least 1 selection",
            instruction="(Select at least 1 and select by pressing on 'Space')",
        ).execute()

        with open(STORED_TG_SPAM_MESSAGES, "r", encoding="utf-8") as f:
            spam_messages = json.loads(f.read())

        if len(spam_messages) == 0:
            raise Exception(
                "You must add least add one spam message to the list of spam messages which is possible by selecting 'Add a Spam Message' option."
            )

        selected_spam_messages: typing.List[str] = inquirer.checkbox(
            "Select the accounts that you want to spam with:",
            spam_messages,
            validate=lambda result: len(result) >= 1,
            invalid_message="Must be at least 1 selection",
            instruction="(Select at least 1 and select by pressing on 'Space')",
        ).execute()

        spam_to_username: str = (
            "@" + inquirer.text("Enter the username that you want to spam: @").execute()
        )

        messages_number: int = int(
            inquirer.number(
                message="How many messages would you like to spam with each account you selected? ",
                min_allowed=1,
                max_allowed=100,
            ).execute()
        )

        color_print(formatted_text=[("red", "STARTED SPAMMING...")])

        asyncio.run(
            helpers.send_message_to(
                list(
                    accounts[selected_account] for selected_account in selected_accounts
                ),
                selected_spam_messages,
                messages_number,
                spam_to_username,
            )
        )

        return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}
