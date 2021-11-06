import discord
import asyncio
import json

from discord.ext import commands

with open('/home/yamin/Coding/Discord/Discord-PY/AngelicBot/cogs/message.json') as file:
    scam_links = json.load(file)

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        autoInv = True
        autoBot = True
        autoScam = True

        if autoScam:
            for scam in scam_links:
                if f"{scam}/" in message.content:
                    em = discord.Embed(
                        title = "No Scam Links",
                        description = "I'm sorry but any message that mentions scam links will get deleted!",
                        color = discord.Color.red()
                    )
                    
                    await message.delete()
                    await message.channel.send(embed=em)
                    return
        
        if autoInv:

            invLink = ["discord.gg", "disboard.org", "top.gg", "disforge.com", "discord.st",
                        "discordservers.com", "discordbee.com", "discordea.net", "discords.com"]

            for link in invLink:
                if f"{link}/" in message.content:
                    getChannel = message.channel
                    getCategory = getChannel.category

                    if getCategory == "╸╸╸ 「 Sponsorships 」 ╺╺╺":
                        return

                    if getCategory == "╸╸╸ 「 Partnerships 」 ╺╺╺":
                        return

                    await message.delete()

                    em = discord.Embed(
                        name = "Warned!",
                        description = "You are not allowed to advertise!",
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
                    
                if category_name == "╸╸╸ 「 Verification 」 ╺╺╺":
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

def setup(bot):
    bot.add_cog(Automod(bot))
    print("-----------------------------------")
    print("( \ ) -- Auto-Mod is ready! -- ( / )")