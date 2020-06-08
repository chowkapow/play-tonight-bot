import discord
import os
import sys

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
env = "prod" if len(sys.argv) == 1 else "dev"
TOKEN = os.getenv("DISCORD_TOKEN") if env == "prod" else os.getenv("dev_DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!",help_command=None)

# !test - Sample command
@bot.command()
async def test(ctx):
    await ctx.send("This is a test command.")

@bot.command()
async def help(ctx):
    await ctx.send('''Help Menu
Schedule time to play league!
Want to contribute? Github
    **!help**
        List Commands
    **!faq**
        Setup and learn how to use this bot
    **!create**
        Start a list/team and specify time using !create n 00:00
        Time is based on 24 hour format i.e. 20:00 is 8pm
    **!teams**
        Shows current team list
    **!join**
        Join team with !join n
    **!leave**
        Leave team with !leave n
    **!edittime**
        Edit time to play with !edittime n 00:00''')


bot.run(TOKEN)
