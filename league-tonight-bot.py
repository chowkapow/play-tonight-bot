import asyncio
import discord
import os
import sys

from datetime import datetime, timedelta
from discord.ext import commands, tasks
from dotenv import load_dotenv

from constants import error_messages as em, help_command as hc
from utils import read_json, write_json

load_dotenv()
env = "prod" if len(sys.argv) == 1 else "dev"
TOKEN = os.getenv("DISCORD_TOKEN") if env == "prod" else os.getenv("dev_DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", help_command=None)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title=hc.get("title"),
        description=hc.get("description"),
        color=discord.Colour.dark_blue(),
    )
    embed.add_field(name=hc.get("help_name"), value=hc.get("help_value"), inline=False)
    embed.add_field(name=hc.get("faq_name"), value=hc.get("faq_value"), inline=False)
    embed.add_field(
        name=hc.get("create_name"), value=hc.get("create_value"), inline=False
    )
    embed.add_field(
        name=hc.get("teams_name"), value=hc.get("teams_value"), inline=False
    )
    embed.add_field(name=hc.get("join_name"), value=hc.get("join_value"), inline=False)
    embed.add_field(
        name=hc.get("leave_name"), value=hc.get("leave_value"), inline=False
    )
    embed.add_field(name=hc.get("edit_name"), value=hc.get("edit_value"), inline=False)
    embed.set_footer(text=hc.get("footer"))
    await ctx.send(embed=embed)


@bot.command()
async def create(ctx, time="7pm"):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data:
        server_teams = data.get(server_id)
        count = len(server_teams)
        if count == 5:
            await ctx.send(em.get("max_teams"))
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
        embed = discord.Embed(title="Teams", color=discord.Colour.dark_blue())
        for t in data[server_id]:
            i = 1
            players = "\n"
            for p in t.get("players"):
                players += "{}. {}\n".format(i, p)
                i += 1
            embed.add_field(
                name="Team " + str(t.get("id")),
                value="Time: " + t.get("time") + players + "--------------------",
                inline=False,
            )
        await ctx.send(embed=embed)
    else:
        await ctx.send(em.get("no_teams"))


@bot.command()
async def join(ctx, id):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data and len(data[server_id]) > 0:
        for t in data[server_id]:
            if str(t.get("id")) == id:
                if ctx.author.name in t.get("players"):
                    await ctx.send(em.get("join_already"))
                    return
                if len(t.get("players")) >= 5:
                    await ctx.send(em.get("full"))
                    return
                t.get("players").append(ctx.author.name)
                write_json(data)
                await teams(ctx)
                return
        await ctx.send(em.get("not_found"))
    else:
        await ctx.send(em.get("no_teams"))


@bot.command()
async def leave(ctx, id):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data and len(data[server_id]) > 0:
        for t in data[server_id]:
            if str(t.get("id")) == id:
                if ctx.author.name not in t.get("players"):
                    await ctx.send(em.get("not_part"))
                else:
                    t.get("players").remove(ctx.author.name)
                    if len(t.get("players")) == 0:
                        data[server_id].remove(t)
                    write_json(data)
                    await ctx.send("You have been removed from team {}.".format(id))
                    await teams(ctx)
                return
        await ctx.send(em.get("not_found"))
    else:
        await ctx.send(em.get("no_teams"))


@bot.command()
async def edit(ctx, id, time):
    server_id = str(ctx.message.guild.id)
    data = read_json("teams.json")
    if server_id in data and len(data[server_id]) > 0:
        for t in data[server_id]:
            if str(t.get("id")) == id:
                if ctx.author.name not in t.get("players"):
                    await ctx.send(em.get("not_part"))
                    return
                t.update({"time": time})
                write_json(data)
                await ctx.send("Team {}'s start time changed to {}".format(id, time))
                await teams(ctx)
                return
        await ctx.send(em.get("not_found"))
    else:
        await ctx.send(em.get("no_teams"))


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
