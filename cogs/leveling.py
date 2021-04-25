import pprint

import discord
import motor.motor_asyncio
import asyncio
import random
import dns

from datetime import datetime
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

cluster = AsyncIOMotorClient("mongodb+srv://vertoxen:omegamemes567@leveldb.tme6j.mongodb.net/?retryWrites=true&w=majority")
db = cluster['leveling']
cursor = db['levels']

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.lvl_channel = self.bot.get_channel(834949731364110336)

    async def process_xp(self, message):
        results = await cursor.find_one({"user_id": message.author.id})
        timeVal = results['xp-lock']
        xp = results['xp']
        lvl = results['level']

        if timeVal == 1:
            await self.add_xp(message, xp)

            await cursor.update_one({"user_id": message.author.id}, {"$set": {"xp-lock": 0}})
            await asyncio.sleep(5)
            await cursor.update_one({"user_id": message.author.id}, {"$set": {"xp-lock": 1}})

    async def add_xp(self, message, xp):
        xp_to_add = random.randint(1, 10)
        newXP = xp + xp_to_add
        date = datetime.utcnow()

        await cursor.update_one({"user_id": message.author.id}, {"$set": {"xp": newXP}})
        await cursor.update_one({"user_id": message.author.id}, {"$set": {"xp-lock": date}})

        results = await cursor.find_one({"user_id": message.author.id})
        cXP = results['xp']
        cReqLvl = results['requireLvl']
        lvl = results['level']

        if cXP >= cReqLvl:
            newLvl = lvl + 1
            newReq = cReqLvl * 3

            await cursor.update_one({"user_id": message.author.id}, {"$set": {"level": newLvl}})
            await cursor.update_one({"user_id": message.author.id}, {"$set": {"requireLvl": newReq}})
            await cursor.update_one({"user_id": message.author.id}, {"$set": {"xp": 0}})

            em = discord.Embed(
                title = "Level Up!",
                description = f"Congrats to {message.author.mention} for leveling up to `Level {newLvl}`!",
                color = discord.Colour.blue()
            )

            em.set_footer(text="Don't forget to stay active!", icon_url=message.author.avatar_url)

            await self.lvl_channel.send(embed=em)
            await self.lvl_channel.send(f"{message.author.mention}", delete_after=1)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            USER_ID = message.author.id
            USER = str(message.author)
            USER_NAME = str(message.author.name)
            USER_DISCRIM = str(message.author.discriminator)

            results = await cursor.find_one({"user_id": USER_ID})

            if results is None:
                ins = {
                    "user_id": USER_ID, "user": USER_NAME, "discriminator": USER_DISCRIM, "level": 1, "xp": 0, "xp-lock": 1,
                    "requireLvl": 50
                }

                await cursor.insert_one(ins)
                pass

            await self.process_xp(message)

    @commands.command(aliases=["level"])
    async def rank(self, ctx):
        USER_ID = ctx.author.id
        USER = str(ctx.author)
        USER_NAME = str(ctx.author.name)

        results = await cursor.find_one({"user_id": USER_ID})

        userLevel = results['level']
        userXP = results['xp']
        userXPCap = results['requireLvl']

        em = discord.Embed(
            title = "Rank!",
            description = f"**{USER_NAME}**'s Rank Info!",
            color = discord.Colour.blue()
        )

        em.add_field(
            name = "Level",
            value = f"`Level {userLevel}`",
            inline = False
        )

        em.add_field(
            name = "XP",
            value = f"`{userXP}xp / {userXPCap}xp`",
            inline = False
        )

        em.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed=em)
        return

    @commands.command(aliases=["levels", "leader", "lead"])
    async def leaderboard(self, ctx):
        em = discord.Embed(
            title = "Error!",
            description = "Commands still in the works!",
            color = discord.Colour.red()
        )

        await ctx.send(embed=em)
        return

def setup(bot):
    bot.add_cog(Leveling(bot))
    print("( \ ) -- Leveling is loaded! -- ( / )")