import discord
import asyncio
import motor.motor_asyncio
import dns

from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

cluster = AsyncIOMotorClient("mongodb+srv://vertoxen:omegamemes567@leveldb.tme6j.mongodb.net/?retryWrites=true&w=majority")
db = cluster['warn']
cursor = db['warnings']

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        USER_ID = message.author.id
        divInvs = True
        divMentions = True

        if not message.author.bot:
            pass



def setup(bot):
    bot.add_cog(Automod(bot))
    print("( \ ) -- Auto-Mod is ready! -- ( / )")