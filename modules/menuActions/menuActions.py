from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
import modules.helpers.helpers as helpers
import json
import asyncio
import modules.types.types as types
from InquirerPy.utils import color_print
from InquirerPy.separator import Separator
from InquirerPy.base import Choice
from modules.static.constants import (
    STORED_TG_USERS,
    STORED_TG_MESSAGES,
    MEDIA_FOLDER,
    GITHUB_ADDRESS,
)
import typing
import os


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
                asyncio.run(helpers.log_out_user(api_id, api_hash, phone_number))
                raise Exception("This account already exists.")

            proceed = inquirer.confirm(
                message=f"Accounts username is @{user_info.username}. Is it OK to continue?",
                default=True,
            ).execute()

            if not proceed:
                asyncio.run(helpers.log_out_user(api_id, api_hash, phone_number))
                raise Exception("Operation aborted.")

            accounts[f"@{user_info.username}"] = {
                "api_id": int(api_id),
                "api_hash": api_hash,
                "phone_number": phone_number,
            }

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


def add_messages_action() -> types.Response:
    message = inquirer.text("Enter your message: ").execute()

    try:
        with open(STORED_TG_MESSAGES, "r+", encoding="utf-8") as f:
            messages: typing.List[str] = json.loads(f.read())

            messages.append(message)

            f.seek(0)
            f.write(json.dumps(messages))
            f.truncate()

            return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}


def show_messages_action() -> types.Response:
    try:
        with open(STORED_TG_MESSAGES, "r", encoding="utf-8") as f:
            messages: typing.List[str] = json.loads(f.read())

            color_print(formatted_text=[("purple", "Added Messages:\n")])

            for message in messages:
                color_print(
                    formatted_text=[
                        ("orange", message + "\n"),
                        ("purple", "___________"),
                    ]
                )

    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}

    try:
        media_files = os.listdir(MEDIA_FOLDER)

        color_print(formatted_text=[("purple", f"Added Medias:\n")])

        for media in media_files:
            color_print(
                formatted_text=[
                    ("orange", media + "\n"),
                    ("purple", "___________"),
                ]
            )
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}

    return {"error": None, "isSuccess": True}


def delete_messages_action() -> types.Response:
    try:
        with open(STORED_TG_MESSAGES, "r", encoding="utf-8") as f:
            messages: typing.List[str] = json.loads(f.read())

        if not messages:
            raise Exception("No text messages to delete.")

        selected_message = inquirer.select(
            message="Select the text message you want to delete:",
            choices=messages,
        ).execute()

        messages.remove(selected_message)

        with open(STORED_TG_MESSAGES, "w", encoding="utf-8") as f:
            f.write(json.dumps(messages))
            f.truncate()

        return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}


def start_auto_messaging_action() -> types.Response:
    try:
        with open(STORED_TG_USERS, "r", encoding="utf-8") as f:
            accounts: typing.Dict[str, types.Account] = json.loads(f.read())

        if len(accounts.keys()) == 0:
            raise Exception(
                "You must add least add one account to the list of accounts which is possible by selecting 'Add a Telegram User' option."
            )

        selected_accounts = inquirer.checkbox(
            "Select the accounts that you want to auto send with:",
            accounts.keys(),
            validate=lambda result: len(result) >= 1,
            invalid_message="Must be at least 1 selection",
            instruction="(Select at least 1 and select by pressing on 'Space')",
        ).execute()

        with open(STORED_TG_MESSAGES, "r", encoding="utf-8") as f:
            text_messages_options = json.loads(f.read())
            text_messages_options = [
                Choice({"type": "text", "data": text_message}, text_message)
                for text_message in text_messages_options
            ]

        media_options = os.listdir(MEDIA_FOLDER)
        media_options = [
            Choice({"type": "media", "data": MEDIA_FOLDER + media_name}, media_name)
            for media_name in media_options
        ]

        if len(text_messages_options) == 0 and len(media_options) == 0:
            raise Exception(
                "You must add least add one message to the list of messages which is possible by selecting 'Add a Message' option."
            )

        selected_message_media_choices: typing.List[types.MessageDict] = (
            inquirer.checkbox(
                "Select the messages and media that you want to auto send:",
                [*text_messages_options, Separator(), *media_options],
                validate=lambda result: len(result) >= 1,
                invalid_message="Must be at least 1 selection",
                instruction="(Select at least 1 and select by pressing on 'Space'. The selected messages will be sent to the specified user randomly)",
            ).execute()
        )

        recipient_username: str = (
            "@"
            + inquirer.text(
                "Enter the username that you want to auto send messages to: @"
            ).execute()
        )

        messages_number: int = int(
            inquirer.number(
                message="How many messages would you like to auto send with each account you selected? ",
                min_allowed=1,
                max_allowed=100,
                float_allowed=False,
                default=None,
                validate=EmptyInputValidator(),
            ).execute()
        )

        color_print(
            formatted_text=[
                (
                    "red",
                    f"Note that each message will be sent from 1 to 5 seconds randomly to decrease the risk of ban. \nSTARTED AUTO SENDING MESSAGES TO {recipient_username}...",
                )
            ]
        )

        asyncio.run(
            helpers.send_message_to(
                {
                    selected_account: accounts[selected_account]
                    for selected_account in selected_accounts
                },
                selected_message_media_choices,
                messages_number,
                recipient_username,
            )
        )

        return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}


def show_github_action() -> types.Response:
    color_print(formatted_text=[("green", GITHUB_ADDRESS)])

    return {"error": None, "isSuccess": True}
