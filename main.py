import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    
    print(f'{bot.user} is now online.')

async def load_extensions():
    cogs_dir = os.path.join(BASE_DIR, 'cogs')
    
    for file in sorted(os.listdir(cogs_dir)):
        if file.endswith('.py') and not file.startswith('_'):
            await bot.load_extension(f'cogs.{file[:-3]}')


async def main():
    if not TOKEN:
        raise RuntimeError('DISCORD_TOKEN is not set.')

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())