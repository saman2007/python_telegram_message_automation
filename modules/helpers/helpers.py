from telethon import TelegramClient, types as telethonTypes
from InquirerPy import inquirer
from modules.static.constants import STORED_TG_USERS
import json
import re


def get_session_path(phone_number: str) -> str:
    return f"sessions/{phone_number[1:]}.session"


async def get_tg_user_info(
    api_id: int, api_hash: str, phone_number: str
) -> telethonTypes.User | telethonTypes.InputPeerUser:
    async def code_callback():
        return await inquirer.text(
            "Enter the code that is sent to your telegram PV: "
        ).execute_async()

    tg_client = TelegramClient(
        get_session_path(phone_number),
        api_id,
        api_hash,
    )

    await tg_client.start(
        phone=phone_number,
        code_callback=code_callback,
    )

    return await tg_client.get_me()


def create_not_existed_data():
    try:
        with open(STORED_TG_USERS, "x") as f:
            f.write("{}")
    except Exception as e:
        pass


def is_user_exist(phone_number: str) -> bool:
    with open(STORED_TG_USERS, "r", encoding="utf-8") as f:
        accounts = json.loads(f.read())

        for account in accounts:
            if phone_number == accounts[account]["phone_number"]:
                return True

        return False


def looks_international(phone_number: str) -> bool:
    return bool(re.fullmatch(r"\+\d{6,15}", phone_number.strip()))


async def log_out_user(api_id: int, api_hash: str, phone_number: str) -> bool:
    tg_client = TelegramClient(get_session_path(phone_number), api_id, api_hash)

    await tg_client.connect()

    return await tg_client.log_out()
