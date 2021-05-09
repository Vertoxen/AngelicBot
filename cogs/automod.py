import discord
import asyncio

from discord.ext import commands

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        autoInv = True
        autoBot = True

        if autoInv:

            invLink = ["discord.gg", "disboard.org", "top.gg", "disforge.com", "discord.st",
                       "discordservers.com", "discordbee.com", "discordea.net", "discords.com"]

            for link in invLink:
                if link in message.content:
                    getChannel = message.channel
                    getCategory = getChannel.category

                    if getCategory == "╸╸╸ 「 Sponsorships 」 ╺╺╺":
                        return

                    if getCategory == "╸╸╸ 「 Partnerships 」 ╺╺╺":
                        return

                    await message.delete()

                    em = discord.Embed(
                        name = "No Advertising!",
                        description = "Advertising is not allowed!",
                        color = discord.Colour.red()
                    )

                    await message.channel.send(embed=em, delete_after=5.0)
                    return

        if autoBot:
            if message.author.bot:
                if isinstance(message.channel, discord.DMChannel):
                    return

                channel = message.channel
                category_name = message.channel.category.name
                channel_name = message.channel.name

                if channel_name == "「➵」-bot-commands":
                    return

                if channel_name == "「➵」-staff-bot-commands":
                    return

                if channel_name == "「➵」-level-up":
                    if message.author.name == "AngelicBot":
                        return

                    else:
                        pass

                if channel_name == "「➵」-ticket-support":
                    return

                if category_name == "╸╸╸ 「 Tickets 」 ╺╺╺":
                    if message.author.name == "AngelicBot":
                        return

                    else:
                        pass

                if channel_name == "「➵」-logs":
                    return

                if channel_name == "「➵」-ticket-logs":
                    if message.author.name == "AngelicBot":
                        return

                    else:
                        pass

                else:
                    await message.delete()

    @commands.command()
    async def test(self, ctx):
        await ctx.send("test")

def setup(bot):
    bot.add_cog(Automod(bot))
    print("( \ ) -- Auto-Mod is ready! -- ( / )")