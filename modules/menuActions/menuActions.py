from InquirerPy import inquirer
import modules.helpers.helpers as helpers
import json
import asyncio
import modules.types.types as types
from InquirerPy.utils import color_print
import os
from modules.static.constants import STORED_TG_USERS, STORED_SESSIONS_FOLDER


def add_tg_user_action() -> types.Response:
    api_id = inquirer.text("Enter your api id: ").execute()
    api_hash = inquirer.text("Enter your api hash: ").execute()

    try:
        user_info = asyncio.run(helpers.get_tg_user_info(int(api_id), api_hash))

        if not user_info:
            raise Exception("No info found.")

        with open(STORED_TG_USERS, "r+", encoding="utf-8") as f:
            accounts = json.loads(f.read())

            if f"@{user_info.username}" in accounts:
                raise Exception("This account already exists.")

            accounts[f"@{user_info.username}"] = {
                "api_id": int(api_id),
                "api_hash": api_hash,
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
                        ("white", "api id: "),
                        ("orange", f"{username}\n"),
                        ("white", "api id: "),
                        ("orange", f"{accounts[username]["api_id"]}\n"),
                        ("white", "api api_hash: "),
                        ("orange", f"{accounts[username]["api_hash"]}\n"),
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
            message="Select an action:",
            choices=accounts.keys(),
        ).execute()

        account_api_id = accounts[selected_username]["api_id"]

        del accounts[selected_username]

        with open(STORED_TG_USERS, "w") as f:
            f.write(json.dumps(accounts))
            f.truncate()

        os.remove(STORED_SESSIONS_FOLDER + f"/{account_api_id}.session")

        return {"error": None, "isSuccess": True}
    except Exception as e:
        return {"error": {"code": 500, "message": str(e)}, "isSuccess": False}
