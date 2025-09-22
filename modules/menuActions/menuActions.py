from InquirerPy import inquirer
import modules.helpers.helpers as helpers
import json
import asyncio
import modules.types.types as types
from InquirerPy.utils import color_print
from modules.static.constants import STORED_TG_USERS, STORED_SESSIONS_FOLDER


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
            accounts = json.loads(f.read())

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
            accounts = json.loads(f.read())

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
            accounts = json.loads(f.read())

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
