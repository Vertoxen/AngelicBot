import discord
import asyncio

from datetime import datetime
from typing import Optional
from discord.ext import commands

FOOTER = "a-help | AngelicNodes"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(833507916321259525)

    @commands.command()
    async def mute(self, ctx, user: discord.Member, hours: int, *, reason: Optional[str] = "No reason provided."):
        USER_NAME = str(ctx.author)
        

        if user is None:
            em = discord.Embed(
                title="Error!",
                description="Please suggest a user that you want to mute!",
                color=discord.Colour.red()
            )

            em.add_field(
                name = "Usage",
                value = "`a-mute {userMention} {insertHours} {reasonText}`",
                inline = False
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

        if hours is None:
            em = discord.Embed(
                title="Error!",
                description="How long do you want to mute the user for? `(1 = 1 hour)`",
                color=discord.Colour.red()
            )

            em.add_field(
                name="Usage",
                value="`a-mute {userMention} {insertHours} {reasonText}`",
                inline=False
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

        if user == ctx.author:
            em = discord.Embed(
                title="Error!",
                description="You cannot mute yourself!",
                color=discord.Colour.red()
            )

            em.add_field(
                name="Usage",
                value="`a-mute {userMention} {insertHours} {reasonText}`",
                inline=False
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

        else:
            OTHER_NAME = str(user)

            sup1 = discord.utils.find(lambda r: r.name == '「 ➣ 」 Support-Lvl 1', ctx.message.guild.roles)
            sup2 = discord.utils.find(lambda r: r.name == '「 ➣ 」 Support-Lvl 2', ctx.message.guild.roles)
            sup3 = discord.utils.find(lambda r: r.name == '「 ➣ 」 Support-Lvl 3', ctx.message.guild.roles)
            manager = discord.utils.find(lambda r: r.name == '「 ➣ 」 Management', ctx.message.guild.roles)
            executives = discord.utils.find(lambda r: r.name == '╸╸╸ 「 Executive 」 ╺╺╺', ctx.message.guild.roles)

            allowed = [sup1, sup2, sup3, manager, executives]

            if allowed in ctx.author.roles:
                if allowed in user.roles:
                    em = discord.Embed(
                        title="Error!",
                        description="The person you are trying to mute is **Staff**!",
                        color=discord.Colour.red()
                    )

                    em.set_footer(text=FOOTER)

                    await ctx.send(embed=em)
                    return

                else:
                    old_roles = discord.utils.get(user.roles)
                    await user.edit(roles=None)
                    role = discord.utils.get(ctx.guild.roles, name='「 ➣ 」 Muted')
                    await user.add_roles(role)

                    em1 = discord.Embed(
                        title="Muted!",
                        description=f"You have successfully muted **{OTHER_NAME}** for **{hours}** hours!",
                        color=discord.Color.green()
                    )

                    em1.set_footer(text=FOOTER)
                    await ctx.send(embed=em1)

                    em2 = discord.Embed(
                        title="Muted!",
                        description="You have been muted in **AngelicNodes**",
                        color=discord.Colour.red()
                    )

                    em2.add_field(
                        name="Duration",
                        value=f"**{hours}** hours",
                        inline=False
                    )

                    em2.add_field(
                        name="Reason",
                        value=f"{reason}",
                        inline=False
                    )

                    em2.set_footer(text=FOOTER)

                    await user.send(embed=em2)

                    emLog = discord.Embed(
                        title="Member Muted!",
                        color=discord.Colour.blue(),
                        timestamp=datetime.utcnow()
                    )

                    emLog.add_field(
                        name="Member",
                        value=f"{OTHER_NAME}",
                        inline=False
                    )

                    emLog.add_field(
                        name="Reason",
                        value=f"`{reason}`",
                        inline=False
                    )

                    emLog.add_field(
                        name="Duration",
                        value=f"**{hours}** hours",
                        inline=False
                    )

                    emLog.add_field(
                        name="Moderator",
                        value=f"{USER_NAME}",
                        inline=False
                    )

                    emLog.set_thumbnail(url=user.avatar_url)

                    await self.log_channel.send(embed=emLog)

                    await asyncio.sleep(hours * 60 * 60)

                    await user.edit(roles=None)
                    await user.add_roles(old_roles)

                    emUn1 = discord.Embed(
                        title="Un-muted!",
                        description="You have been un-muted in **AngelicNodes**!",
                        color=discord.Colour.green()
                    )

                    emUn1.set_footer(text=FOOTER)

                    await user.send(embed=emUn1)

                    emLogUn = discord.Embed(
                        title="Member Un-muted!",
                        color=discord.Color.random(),
                        timestamp=datetime.utcnow()
                    )

                    emLogUn.add_field(
                        name="Member",
                        value=f"{OTHER_NAME}",
                        inline=False
                    )

                    emLogUn.add_field(
                        name="Muted",
                        value=f"**{hours}** hours ago!",
                        inline=False
                    )

                    emLogUn.set_thumbnail(url=user.avatar_url)

                    await self.log_channel.send(embed=emLogUn)
                    return

            else:
                em = discord.Embed(
                    title="Error!",
                    description="You do not have permission to use this command!",
                    color=discord.Colour.red()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason: Optional[str] = "No reason provided."):
        if ctx.message.author.guild_permissions.ban_members:
            if user is None:
                em = discord.Embed(
                    title = "Error!",
                    description = "Please mention the user that you want to ban!",
                    color = discord.Colour.red()
                )

                em.add_field(
                    name="Usage",
                    value="`a-ban {userMention} {reasonText}`",
                    inline=False
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

            if user.top_role >= ctx.author.top_role:
                em = discord.Embed(
                    title="Error!",
                    description="You can only ban people below your role!",
                    color=discord.Colour.red()
                )

                em.add_field(
                    name = "Usage",
                    value = "`a-ban {userMention} {reasonText}`",
                    inline = False
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

            if user == ctx.author:
                em = discord.Embed(
                    title="Error!",
                    description="You cannot ban yourself!",
                    color=discord.Colour.red()
                )

                em.add_field(
                    name = "Usage",
                    value = "`a-ban {userMention} {reasonText}`",
                    inline = False
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

            else:
                emDM = discord.Embed(
                    title="Banned!",
                    description="You have been banned!",
                    color=discord.Colour.red()
                )

                emDM.add_field(
                    name="Server",
                    value="AngelicNodes",
                    inline=False
                )

                emDM.add_field(
                    name="Reason",
                    value=f"{reason}",
                    inline=False
                )

                emDM.set_footer(text=FOOTER)
                emDM.set_thumbnail(url=ctx.guild.icon_url)

                await user.send(embed=emDM)

                emLog = discord.Embed(
                    title="Member Banned!",
                    color=discord.Colour.blue(),
                    timestamp=datetime.utcnow()
                )

                emLog.add_field(
                    name="User",
                    value=f"{user}",
                    inline=False
                )

                emLog.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False
                )

                emLog.add_field(
                    name="Reason",
                    value=f"`{reason}`",
                    inline=False
                )

                emLog.set_thumbnail(url=user.avatar_url)

                await self.log_channel.send(embed=emLog)

                await user.ban(reason=reason)

                em = discord.Embed(
                    title="Banned!",
                    description=f"**{user}** has been banned! This will be logged!",
                    color=discord.Colour.green()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)
                return

        else:
            em = discord.Embed(
                title="Error!",
                description="You don't have permission to use this command!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

    @commands.command()
    async def unban(self, ctx, id: int = None):
        if ctx.message.author.guild_permissions.administrator:
            if id is None:
                em = discord.Embed(
                    title="Error!",
                    description="Please input an ID of a user that you are going to unban!",
                    color=discord.Colour.red()
                )

                em.add_field(
                    name = "Usage",
                    value = "`a-unban {userID}`",
                    inline = False
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

            else:
                user = await self.bot.fetch_user(id)

                banned_users = await ctx.guild.bans()
                member_name, member_discriminator = user.split('#')

                for ban_entry in banned_users:
                    member = ban_entry.banned_users

                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await ctx.guild.unban(user)

                        em = discord.Embed(
                            title="Unbanned!",
                            description=f"**{user}** has successfully gotten unbanned!",
                            color=discord.Colour.green()
                        )

                        em.set_footer(text=FOOTER)

                        await ctx.send(embed=em)

                        emLog = discord.Embed(
                            title="Member Unbanned!",
                            color=discord.Colour.blue(),
                            timestamp=datetime.utcnow()
                        )

                        emLog.add_field(
                            name="User",
                            value=f"{user}",
                            inline=False
                        )

                        emLog.add_field(
                            name="Moderator",
                            value=f"{ctx.author}",
                            inline=False
                        )

                        emLog.set_thumbnail(url=user.avatar_url)

                        await self.log_channel.send(embed=emLog)
                        return

                    else:
                        em = discord.Embed(
                            title="Error!",
                            description="The user you mentioned **is not banned/cannot be found**!",
                            color=discord.Colour.red()
                        )

                        em.set_footer(text=FOOTER)

                        await ctx.send(embed=em, delete_after=5.0)
                        await asyncio.sleep(5.0)
                        await ctx.message.delete()

                        return

        else:
            em = discord.Embed(
                title="Error!",
                description="You don't have permission to use this command!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason: Optional[str] = "No reason provided."):
        if ctx.message.author.guild_permissions.kick_members:
            if user is None:
                em = discord.Embed(
                    title = "Error!",
                    description = "Please mention the user that you are trying to kick!",
                    color = discord.Colour.red()
                )

                em.add_field(
                    name = "Usage",
                    value = "`a-kick {userMention} {reasonText}`",
                    inline = False
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

            if user.top_role >= ctx.author.top_role:
                em = discord.Embed(
                    title="Error!",
                    description="You can only kick people below your role!",
                    color=discord.Colour.red()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)
                return

            if user == ctx.author:
                em = discord.Embed(
                    title="Error!",
                    description="You cannot kick yourself!",
                    color=discord.Colour.red()
                )

                em.add_field(
                    name = "Usage",
                    value = "`a-kick {userMention} {reasonText}`",
                    inline = False
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

            else:
                emDM = discord.Embed(
                    title="Kicked!",
                    description="You have been kicked!",
                    color=discord.Colour.red()
                )

                emDM.add_field(
                    name="Server",
                    value="AngelicNodes",
                    inline=False
                )

                emDM.add_field(
                    name="Reason",
                    value=f"{reason}",
                    inline=False
                )

                emDM.set_footer(text=FOOTER)
                emDM.set_thumbnail(url=ctx.guild.icon_url)

                await user.send(embed=emDM)

                emLog = discord.Embed(
                    title="Member Kicked!",
                    color=discord.Colour.blue(),
                    timestamp=datetime.utcnow()
                )

                emLog.add_field(
                    name="User",
                    value=f"{user}",
                    inline=False
                )

                emLog.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False
                )

                emLog.add_field(
                    name="Reason",
                    value=f"`{reason}`",
                    inline=False
                )

                emLog.set_thumbnail(url=user.avatar_url)

                await self.log_channel.send(embed=emLog)

                await user.kick(reason=reason)

                em = discord.Embed(
                    title="Banned!",
                    description=f"**{user}** has been kicked! This will be logged!",
                    color=discord.Colour.green()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)
                return

        else:
            em = discord.Embed(
                title="Error!",
                description="You don't have permission to use this command!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

    @commands.command(aliases=["clear"])
    async def purge(self, ctx, amount: int = None):
        if ctx.message.author.guild_permissions.manage_messages:
            if amount is None:
                em = discord.Embed(
                    title = "Error!",
                    description = "Please insert in the amount of messages that you are going to purge!",
                    color = discord.Colour.red()
                )

                em.add_field(
                    name = "Usage",
                    value = "`a-purge {purgeAmount}`"
                )

                em.set_footer(text = FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                await asyncio.sleep(5.0)
                await ctx.message.delete()

                return

            else:
                await ctx.message.delete()
                await ctx.channel.purge(limit=amount)

                em = discord.Embed(
                    title = "Purged!",
                    description = f"**{amount} messages** have successfully gotten purged!",
                    color = discord.Colour.blue()
                )

                em.set_footer(text = FOOTER)

                await ctx.send(embed=em, delete_after=5.0)
                return

        else:
            em = discord.Embed(
                title="Error!",
                description="You don't have permission to use this command!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

    @commands.command(aliases=["purgeall", "clearall"])
    async def nuke(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            channel = ctx.channel

            await channel.purge(limit=999999999)

            em = discord.Embed(
                title = "Nuked!",
                description = "The chat has been nuked!",
                color = discord.Colour.green()
            )

            await channel.send(embed=em, delete_after=5.0)
            return

        else:
            em = discord.Embed(
                title = "Error!",
                description = "You don't have permission to execute this command!",
                color = discord.Colour.red()
            )

            await ctx.send(embed=em, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()

            return

def setup(bot):
    bot.add_cog(Moderation(bot))
    print("( \ ) -- Moderation is loaded! -- ( / )")