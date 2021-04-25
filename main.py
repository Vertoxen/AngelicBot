import discord
import os
import asyncio

from discord.ext import commands
from itertools import cycle

intents = discord.Intents.all()
client = commands.Bot(command_prefix="a-", intents=intents)

TOKEN = "ODM0MTA1MDc4NjYyMDM3NTc1.YH8C4w.ATlSr5-Ft7AyGA1rHEl1-PxXrnU"
INVITE = "https://discord.com/api/oauth2/authorize?client_id=822632273278140466&permissions=201714753&scope=bot"
STATUS = [f"a-help | AngelicNodes", "all the users! | AngelicNodes"]

os.chdir(r"/home/yaminahmed47/Coding Folder/Python/AngelicBot")

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(STATUS)

    while not client.is_closed():
        current_status = next(msgs)
        activity = discord.Activity(type=discord.ActivityType.watching, name=current_status)
        await client.change_presence(status=discord.Status.dnd, activity=activity)
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print("( \ ) -- Bot is ready! -- ( / )")

for filename in os.listdir(f"./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.loop.create_task(change_status())
client.run(TOKEN)
