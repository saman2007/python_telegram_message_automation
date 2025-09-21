from telethon import TelegramClient, types as telethonTypes
from InquirerPy import inquirer
import modules.types.types as types


async def get_tg_user_info(
    api_id: int, api_hash: str
) -> telethonTypes.User | telethonTypes.InputPeerUser:
    async def get_phone():
        return await inquirer.text("Enter your phone number: ").execute_async()

    async def code_callback():
        return await inquirer.text(
            "Enter the code that is sent to your telegram PV: "
        ).execute_async()

    tg_client = TelegramClient(
        f"sessions/{api_id}.session",
        api_id,
        api_hash,
    )

    await tg_client.start(
        phone=get_phone,
        code_callback=code_callback,
    )

    return await tg_client.get_me()
