import discord
import asyncio

from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.welcome_channel = self.bot.get_channel(834155216227532842)
        self.leave_channel = self.bot.get_channel(834155253850308648)
        self.server_guild = self.bot.get_guild(832361964725993532)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        member_count = len([m for m in self.server_guild.members if not m.bot])

        if not member.bot:
            normal = discord.utils.get(member.guild.roles, name='╸╸╸ 「 Normal 」 ╺╺╺')
            user = discord.utils.get(member.guild.roles, name='「 ➣ 」 User')
            ping = discord.utils.get(member.guild.roles, name='╸╸╸ 「 Ping 」 ╺╺╺')

            await member.add.roles(normal)
            await member.add_roles(user)
            await member.add_roles(ping)

            emChannel = discord.Embed(
                title = "Welcome!",
                description = f"**{member.mention}** has joined the server! We are now at **{member_count} members**!",
                color = discord.Colour.blue()
            )

            emChannel.set_footer(text="Please check out #「➵」-verify !", icon_url=member.avatar_url)
            emChannel.set_thumbnail(url=member.avatar_url)

            await self.welcome_channel.send(embed=emChannel)

            emDM = discord.Embed(
                title = "Welcome to AngelicNodes!",
                description = f"Hi there **{member.name}**! I would like to personally welcome you to **AngelicNodes** "
                              f"even though I am a bot! Please have a look around, maybe look at the rules, after you "
                              f"have verified yourself! Don't know how? It's as simple as reading the steps that are "
                              f"written in <#834200691912081458>! Good luck!",
                color = discord.Colour.blue()
            )

            emDM.add_field(
                name = "Links",
                value = "Client Area ➵ **https://client.angelicnodes.net**\nPanel Area ➵ **https://panel.angelicnodes.net**",
                inline = False
            )

            emDM.set_footer(text="Enjoy yourself!", icon_url=member.avatar_url)

            await member.send(embed=emDM)

        else:
            bots = discord.utils.get(member.guild.roles, name='「 ➣ 」 Bots')
            normal = discord.utils.get(member.guild.roles, name='╸╸╸ 「 Normal 」 ╺╺╺')

            await member.add_roles(bots)
            await member.add_roles(normal)

            await member.edit(nick=f"( ) {member.name}")

            em = discord.Embed(
                title = "Welcome!",
                description=f"**{member.name}** has joined us! It seems like it's a bot!",
                color = discord.Colour.green()
            )

            em.set_footer(text="Bots are important for a Discord server!")

            await self.welcome_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        member_count = len([m for m in self.server_guild.members if not m.bot])

        if not member.bot:
            em = discord.Embed(
                title = "Oh...",
                description = f"**{member.name}#{member.discriminator}** has sadly left us... We are now at **{member_count} members**.",
                color = discord.Colour.blue()
            )

            em.set_footer(text = "Hope they come back to us one day...")

            await self.leave_channel.send(embed=em)

        else:
            em = discord.Embed(
                title = "Oh...",
                description = f"The bot **{member.name}** sadly no longer has any purpose...",
                color = discord.Colour.red()
            )

            em.set_footer(text="It just means that we've got something better!")

            await self.leave_channel.send(embed=em)

def setup(bot):
    bot.add_cog(Welcome(bot))
    print("( \ ) -- Welcome is loaded! -- ( / )")