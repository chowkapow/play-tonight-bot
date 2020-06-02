import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")

# !test - Sample command
@bot.command()
async def test(ctx):
    await ctx.send("This is a test command.")


bot.run(TOKEN)
