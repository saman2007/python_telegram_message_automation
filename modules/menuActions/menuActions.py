from InquirerPy import inquirer
import modules.helpers.helpers as helpers
import json
import asyncio
import modules.types.types as types


def add_tg_user_action() -> types.Response:
    api_id = inquirer.text("Enter your api id: ").execute()
    api_hash = inquirer.text("Enter your api hash: ").execute()

    try:
        user_info = asyncio.run(helpers.get_tg_user_info(int(api_id), api_hash))

        if not user_info:
            raise Exception("No info found.")

        with open("data/data.json", "r+", encoding="utf-8") as f:
            accounts = json.loads(f.read())

            if(f"@{user_info.username}" in accounts):
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
