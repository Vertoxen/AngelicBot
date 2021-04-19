import discord
import os
import asyncio

from discord.ext import commands
from itertools import cycle

intents = discord.Intents.all()
client = commands.Bot(command_prefix="a-", intents=intents)

TOKEN = "ODIyNjMyMjczMjc4MTQwNDY2.YFVGAQ.sNs3Za9usObI6SZtbKmdvqitWiE"
INVITE = "https://discord.com/api/oauth2/authorize?client_id=822632273278140466&permissions=201714753&scope=bot"
true_member_count = len([m for m in ctx.guild.members if not m.bot])
STATUS = [f"a-help | AngelicNodes", f"{true_member_count} users | AngelicNodes"]

os.chdir(r"/home/yaminahmed/Python/Captial-Empire")

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(STATUS)

    while not client.is_closed():
        current_status = next(msgs)
        activity = discord.Game(name=current_status)
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
