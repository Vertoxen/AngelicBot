import datetime
import discord
import asyncio
import motor.motor_asyncio
import aiosqlite

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from discord.ext import commands

cluster = AsyncIOMotorClient("mongodb+srv://vertoxen:omegamemes567@leveldb.tme6j.mongodb.net/?retryWrites=true&w=majority")

cdb = cluster['count']
counter = cdb['counter']

db = aiosqlite.connect('warn.sqlite')
count = aiosqlite.connect('count.sqlite')

FOOTER = "a-help | AngelicNodes"

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await db
        await count

        cursor = await db.cursor()
        counter = await count.cursor()

        await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS main(
                        num INTEGER NOT NULL PRIMARY KEY,
                        caseNum INTEGER NOT NULL,
                        reason TEXT,
                        user_id INTEGER NOT NULL,
                        user_name TEXT,
                        user_disc TEXT,
                        moderator TEXT
                    )
                """)
        await db.commit()

        await counter.execute("""
                CREATE TABLE IF NOT EXISTS main(
                    id INTEGER NOT NULL,
                    countNum INTEGER NOT NULL
                )
        """)
        await count.commit()

    @commands.command()
    async def warn(self, ctx, member: discord.Member = None, *, reason: Optional[str] = "No reason provided."):
        if ctx.message.author.guild_permissions.manage_messages:
            cursor = await db.cursor()
            counter = await count.cursor()

            if member is None:
                em = discord.Embed(
                    title = "Error!",
                    description = "Please mention the member that you are trying to warn!",
                    color = discord.Colour.red()
                )

                em.add_field(
                    name = "Usage",
                    value = "`a-warn {userMention} {reasonText}`",
                    inline = False
                )

                await ctx.send(embed=em)
                return

            if ctx.author == member:
                em = discord.Embed(
                    title="Error!",
                    description="You cannot warn yourself!",
                    color=discord.Colour.red()
                )

                em.add_field(
                    name="Usage",
                    value="`a-warn {userMention} {reasonText}`",
                    inline=False
                )

                await ctx.send(embed=em)
                return

            else:
                try:
                    moderator = str(ctx.author)

                    await counter.execute("SELECT countNum FROM main WHERE id=1")
                    oldCount = await counter.fetchone()

                    if oldCount is None:
                        id = 1
                        numA = 1

                        await counter.execute(
                            "INSERT INTO main(id, countNum) values(?, ?)",
                            (id, numA)
                        )
                        await count.commit()

                    id = 1

                    await counter.execute(f"SELECT countNum FROM main WHERE id={id}")
                    res_countNum = await counter.fetchone()

                    num = res_countNum[0]

                    await cursor.execute(
                        "INSERT INTO main(caseNum, reason, user_id, user_name, user_disc, moderator) values(?, ?, ?, ?, ?, ?)",
                        (num, reason, member.id, member.name, member.discriminator, moderator)
                    )
                    await db.commit()

                    await counter.execute(f"UPDATE main SET countNum = countNum + 1 WHERE id={id}")
                    await count.commit()

                    em = discord.Embed(
                        title = "Warned!",
                        description = f"`Case #{num}`",
                        color = discord.Colour.orange(),
                        timestamp = datetime.datetime.utcnow()
                    )

                    em.add_field(
                        name = "User",
                        value = f"{str(member)}",
                        inline = False
                    )

                    em.add_field(
                        name = "Reason",
                        value = f"{reason}",
                        inline = True
                    )

                    em.add_field(
                        name = "Moderator",
                        value = f"{moderator}",
                        inline = False
                    )

                    await ctx.send(embed=em)
                    await member.send(embed=em)
                    return

                except Exception as key:
                    em = discord.Embed(
                        title = "Error!",
                        description = "An error has occurred while trying to warn this user!",
                        color = discord.Colour.red()
                    )

                    em.add_field(
                        name = "Type",
                        value = "`DB Error`",
                        inline = False
                    )

                    await ctx.send(embed=em)

                    print(key)
                    return

    @commands.command(aliases=["warns"])
    async def warnings(self, ctx, member: discord.Member = None):
        cursor = await db.cursor()

        if member is None:
            USER_ID = ctx.author.id

            await cursor.execute(f"SELECT * FROM main WHERE user_id={USER_ID}")
            result_userInfo = await cursor.fetchall()

            if result_userInfo is None:
                em = discord.Embed(
                    title = "Warnings!",
                    description = "You currently have no warnings!",
                    color = discord.Colour.green()
                )

                await ctx.send(embed=em)
                return

            else:
                em = discord.Embed(
                    title = "Warnings!",
                    color = discord.Colour.orange()
                )

                for i, x in enumerate(result_userInfo, 0):
                    em.add_field(
                        name = f"Case #{x[1]}",
                        value = f"**Reason:** {x[2]}\n**Moderator:** {x[6]}",
                        inline = False
                    )

                await ctx.send(embed=em)
                return

def setup(bot):
    bot.add_cog(Warn(bot))
    print("( \ ) -- Warn is loaded! -- ( / )")