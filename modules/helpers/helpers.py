from telethon import TelegramClient, types as telethonTypes
import asyncio


async def get_tg_user_info(
    api_id: int, api_hash: str
) -> telethonTypes.User | telethonTypes.InputPeerUser:
    tg_client = await TelegramClient("anon", api_id, api_hash).start()
    user_info = await tg_client.get_me()

    return user_info
