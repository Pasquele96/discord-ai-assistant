import discord
from discord.ext import commands
import asyncio
from bot.bot import AIAssistantBot
from config import TOKEN

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = AIAssistantBot(command_prefix='!', intents=intents)
    
    async with bot:
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())