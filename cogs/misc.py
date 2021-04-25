import discord
import asyncio
import aiosqlite

from typing import Optional
from discord.ext import commands
from discord.ext.commands import BucketType
from datetime import datetime, timedelta

db = aiosqlite.connect('counter.sqlite')


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await db

        cursor = await db.cursor()

        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS main(
                num INTEGER NOT NULL,
                counter INTEGER NOT NULL
            )
        """)
        await db.commit()

        await cursor.execute("SELECT counter FROM main WHERE num = 1")
        result = await cursor.fetchone()

        if result is None:
            num = 0
            one = 1

            await cursor.execute("INSERT INTO main(num, counter) values(1, 0)")
            await db.commit()

        self.suggest_channel = self.bot.get_channel(833436390112231474)
        self.ad_channel = self.bot.get_channel(835691260911943730)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            sec = timedelta(seconds=int(error.retry_after))
            d = datetime(1, 1, 1) + sec

            em = discord.Embed(
                title="Cooldown!",
                description=f"Please wait for `{d.day - 1}days {d.hour}hours {d.minute}mins {d.second}seconds`!",
                color=discord.Colour.red()
            )

            await ctx.send(embed=em)
            return

    @commands.command()
    async def suggest(self, ctx, *, msg=None):
        if msg is None:
            em = discord.Embed(
                title="Error!",
                description="No Suggestion Given!",
                color=discord.Colour.red()
            )

            em.add_field(
                name="Usage",
                value="`a-suggest {suggestMessage}`",
                inline=False
            )

            await ctx.send(embed=em)
            return

        else:
            cursor = await db.cursor()

            em = discord.Embed(
                title="Successful!",
                description="Your suggestion has successfully been sent!",
                color=discord.Colour.blue()
            )

            await ctx.send(embed=em)

            await cursor.execute("SELECT counter FROM main WHERE num = 1")
            results = await cursor.fetchone()
            num = results[0]

            await cursor.execute("UPDATE main SET counter = counter + 1 WHERE num = 1")
            await db.commit()

            await cursor.execute("SELECT counter FROM main WHERE num=1")
            newRes = await cursor.fetchone()
            newNum = newRes[0]

            emSuggest = discord.Embed(
                title=f"Suggestion #{newNum}",
                description=f"{msg}",
                color=discord.Colour.blue())

            emSuggest.set_thumbnail(url=ctx.author.avatar_url)
            emSuggest.set_footer(text=f"Suggestion by {str(ctx.author)}!", icon_url=ctx.author.avatar_url)

            await self.suggest_channel.send(embed=emSuggest)
            return

    @commands.command(aliases=['ad'])
    @commands.cooldown(1, 60 * 60 * 60 * 3, BucketType.user)
    async def advertise(self, ctx, inv: discord.Invite = None, *, desc: Optional[str] = "No Description Provided!"):
        if discord.Invite is None:
            em = discord.Embed(
                title="Error!",
                description="No Invite Link Found!",
                color=discord.Colour.red()
            )

            em.add_field(
                name="Usage",
                value="`a-advertise {inviteLink} {descriptionText}`",
                inline=False
            )

            await ctx.send(embed=em)
            return

        else:
            emAd = discord.Embed(
                title=f"{inv.guild.name}",
                url=f"{inv.url}",
                timestamp=datetime.utcnow(),
                color=discord.Colour.blue()
            )

            emAd.add_field(
                name="Description",
                value=f"{desc}",
                inline=False
            )

            emAd.set_thumbnail(url=inv.guild.icon_url)

            await self.ad_channel.send(embed=emAd)

            em = discord.Embed(
                title="Successful!",
                description="Your ad has successfully been posted!",
                color=discord.Colour.green()
            )

            await ctx.send(embed=em)
            return


def setup(bot):
    bot.add_cog(Misc(bot))
    print("( \ ) -- Misc has loaded -- ( / )")
