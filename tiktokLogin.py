from tiktokpy import TikTokPy
import asyncio

async def login():
    async with TikTokPy() as bot:
        await bot.login_session()

asyncio.run(login())
