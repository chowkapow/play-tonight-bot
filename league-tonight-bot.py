import discord
import os
import sys

from datetime import datetime, timedelta
from discord.ext import commands, tasks
from dotenv import load_dotenv
from utils import read_json, write_json

load_dotenv()
env = "prod" if len(sys.argv) == 1 else "dev"
TOKEN = os.getenv("DISCORD_TOKEN") if env == "prod" else os.getenv("dev_DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", help_command=None)


@bot.command()
async def help(ctx):
    await ctx.send(
        """Help Menu
Schedule time to play league!
Want to contribute? Github
    **!help**
        List commands
    **!create**
        Create a team with __!create__ or __!create time__
        Default start time is 7pm
        __!create 8pm__ will create a team with start time 8pm
        Max of 5 teams can be created
    **!teams**
        Show current teams
    **!join**
        Join team with __!join n__
    **!leave**
        Leave team with __!leave n__
    **!edit**
        Edit time to play with __!edit n time__
        __!edit 2 9pm__ will change Team 2's start time to 9pm
        You must be part of the team to edit the time
        """
    )


@bot.command()
async def create(ctx, time="7pm"):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data:
        server_teams = data.get(server_id)
        count = len(server_teams)
        if count == 5:
            await ctx.send("Max of 5 teams reached! Please try again later.")
            return
        else:
            id = int(server_teams[count - 1].get("id")) + 1 if count > 0 else 1
            new_team = {"id": id, "time": time, "players": [ctx.author.name]}
            server_teams.append(new_team)
    else:
        id = 1
        data[server_id] = [{"id": 1, "time": time, "players": [ctx.author.name]}]

    write_json(data)
    await ctx.send("Created team {}.".format(id))
    await teams(ctx)


@bot.command()
async def teams(ctx):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data and len(data[server_id]) > 0:
        list_of_teams = "**TEAMS**\n"
        for t in data[server_id]:
            i = 1
            players = "\n"
            for p in t.get("players"):
                players += "\t{}. {}\n".format(i, p)
                i += 1
            list_of_teams += "**Team {}**\n**Time**: {}\n**Players** {}".format(
                t.get("id"), t.get("time"), players
            )
            list_of_teams += "\n"
        await ctx.send(list_of_teams)
    else:
        await ctx.send("No teams exist!")


@bot.command()
async def join(ctx, id):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data and len(data[server_id]) > 0:
        for t in data[server_id]:
            if str(t.get("id")) == id:
                t.get("players").append(ctx.author.name)
                write_json(data)
                await teams(ctx)
            else:
                await ctx.send("Team not found!")
    else:
        await ctx.send("No teams exist!")


@bot.command()
async def leave(ctx, id):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data and len(data[server_id]) > 0:
        for t in data[server_id]:
            if str(t.get("id")) == id and ctx.author.name in t.get("players"):
                t.get("players").remove(ctx.author.name)
                await ctx.send("You have been removed from team {}.".format(id))
                await teams(ctx)
                write_json(data)
            else:
                await ctx.send("You are not found in the specified team!")
    else:
        await ctx.send("No teams exist!")


@bot.command()
async def edit(ctx, id, time):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data:
        server_teams = data.get(server_id)
        i = 0
        while i < len(server_teams):
            team = server_teams[i]
            if int(team.get("id")) == int(id):
                if ctx.author.name not in team.get("players"):
                    await ctx.send("You are not part of this team!")
                    return
                team.update({"time": time})
                write_json(data)
                await ctx.send("Team {}'s start time changed to {}".format(id, time))
                await teams(ctx)
                return
            i += 1
        await ctx.send("Team {} does not exist!".format(id))
    else:
        await ctx.send("No teams exist!")


@tasks.loop(hours=24)
async def reset_teams():
    write_json({})


@reset_teams.before_loop
async def before():
    d = datetime.now()
    if d.hour < 3:
        reset = datetime(
            year=d.year, month=d.month, day=d.day, hour=3, minute=0, second=0
        )
    else:
        tomorrow = d + timedelta(days=1)
        reset = datetime(
            year=tomorrow.year,
            month=tomorrow.month,
            day=tomorrow.day,
            hour=3,
            minute=0,
            second=0,
        )
    await asyncio.sleep((reset - d).total_seconds())
    await bot.wait_until_ready()


reset_teams.start()

bot.run(TOKEN)
