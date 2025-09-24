from telethon import TelegramClient, types as telethonTypes
from InquirerPy import inquirer
from modules.static.constants import (
    STORED_TG_USERS,
    STORED_TG_SPAM_MESSAGES,
    MEDIA_FOLDER,
)
import json
import re
import typing
import modules.types.types as types
import asyncio
from random import choice, randint
import os
from InquirerPy.utils import color_print


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


def initialize():
    try:
        os.makedirs(MEDIA_FOLDER)
    except FileExistsError as e:
        pass

    try:
        with open(STORED_TG_USERS, "x") as f:
            f.write("{}")
    except FileExistsError as e:
        pass

    try:
        with open(STORED_TG_SPAM_MESSAGES, "x") as f:
            f.write("[]")
    except FileExistsError as e:
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


async def send_message_to(
    accounts: typing.Dict[str, types.Account],
    messages: typing.List[str],
    messages_number: int,
    spam_to: str,
) -> None:
    sent_messages: int = 0

    def print_sent_messages(username: str) -> None:
        print(
            f"\033[94mSent {sent_messages} out of {messages_number} by {username}.\033[0m",
            end="\n",
        )

    for username in accounts:
        account = accounts[username]
        sent_messages = 0

        tg_client = TelegramClient(
            get_session_path(account["phone_number"]),
            account["api_id"],
            account["api_hash"],
        )

        await tg_client.connect()

        for i in range(0, messages_number):
            random_msg = choice(messages)

            if i == 0:
                print_sent_messages(username)
                print("\033[F\033[K", end="")

            await tg_client.send_message(spam_to, random_msg)

            sent_messages += 1
            print_sent_messages(username)

            if i != messages_number - 1:
                wait_time = randint(1, 5)
                print(f"\033[94mWaiting for {wait_time} s.\033[0m", end="\n")
                await asyncio.sleep(wait_time)
                print("\033[F\033[K", end="")
                print("\033[F\033[K", end="")
