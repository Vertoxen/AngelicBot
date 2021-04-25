import discord
import asyncio
from discord.ext import commands
from datetime import datetime


class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(833507916321259525)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.discriminator != after.discriminator:
            em = discord.Embed(
                title="Discriminator Changed!",
                color=discord.Colour.blue(),
                timestamp=datetime.utcnow()
            )

            em.add_field(
                name="Before",
                value=f"{before.name}**#{before.discriminator}**",
                inline=False
            )
            em.add_field(
                name="After",
                value=f"{after.name}**#{after.discriminator}**",
                inline=False
            )
            em.set_thumbnail(url=after.avatar_url)

            if self.log_channel is not None:
                await self.log_channel.send(embed=em)

        if before.name != after.name:
            em = discord.Embed(
                title="Username Changed!",
                color=discord.Colour.blue(),
                timestamp=datetime.utcnow()
            )

            em.add_field(
                name="Before",
                value=f"**{before.name}**#{before.discriminator}",
                inline=False
            )
            em.add_field(
                name="After",
                value=f"**{after.name}**#{after.discriminator}",
                inline=False
            )
            em.set_thumbnail(url=after.avatar_url)

            if self.log_channel is not None:
                await self.log_channel.send(embed=em)

        if before.avatar_url != after.avatar_url:
            em = discord.Embed(
                title="Avatar Changed!",
                description=f"User **{after.name}#{after.discriminator}** changed their avatar!",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )

            em.set_thumbnail(url=before.avatar_url)
            em.set_image(url=after.avatar_url)

            if self.log_channel is not None:
                await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                em = discord.Embed(
                    title="Message Edited!",
                    description=f"Message edited by **{after.author.name}#{after.author.discriminator}**",
                    color=discord.Colour.blue(),
                    timestamp=datetime.utcnow()
                )

                em.add_field(
                    name="Before",
                    value=f"`{before.content}`",
                    inline=False
                )

                em.add_field(
                    name="After",
                    value=f"`{after.content}`",
                    inline=False
                )
                em.set_thumbnail(url=after.author.avatar_url)

                if self.log_channel is not None:
                    await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            em = discord.Embed(
                title="Nickname Changed!",
                color=discord.Colour.blue(),
                timestamp=datetime.utcnow()
            )

            em.add_field(
                name="Before",
                value=f"{before.display_name}",
                inline=False
            )

            em.add_field(
                name="After",
                value=f"{after.display_name}",
                inline=False
            )
            em.set_thumbnail(url=after.avatar_url)

            if self.log_channel is not None:
                await self.log_channel.send(embed=em)

        elif before.roles != after.roles:
            em = discord.Embed(
                title="Member Roles Updated!",
                color=discord.Colour.blue(),
                timestamp=datetime.utcnow()
            )

            em.add_field(
                name="Before",
                value=", ".join([r.mention for r in before.roles]),
                inline=False
            )
            em.add_field(
                name="After",
                value=", ".join([r.mention for r in after.roles]),
                inline=False
            )
            em.set_thumbnail(url=after.avatar_url)

            if self.log_channel is not None:
                await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            em = discord.Embed(
                title="Message Deleted!",
                description=f"Message deleted by **{message.author.name}#{message.author.discriminator}**",
                color=discord.Colour.blue(),
                timestamp=datetime.utcnow()
            )

            em.add_field(
                name="Message",
                value=f"`{message.content}`"
            )
            em.set_thumbnail(url=message.author.avatar_url)

            if self.log_channel is not None:
                await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name != after.name:
            em = discord.Embed(
                title="Server Title Updated!",
                timestamp=datetime.utcnow(),
                color=discord.Colour.blue()
            )

            em.add_field(
                name="Before",
                value=f"`{before}`",
                inline=False
            )

            em.add_field(
                name="After",
                value=f"`{after}`"
            )

            await self.log_channel.send(embed=em)

        if before.icon_url != after.icon_url:
            em = discord.Embed(
                title="Server Icon Updated!",
                timestamp=datetime.utcnow(),
                color=discord.Colour.blue()
            )

            em.set_thumbnail(url=before.icon_url)
            em.set_image(url=after.icon_url)

            await self.log_channel.send(embed=em)

        if before.region != after.region:
            em = discord.Embed(
                title="Server Region Updated!",
                timestamp=datetime.utcnow(),
                color=discord.Colour.blue()
            )

            em.add_field(
                name="Before",
                value=f"`{before.region}`",
                inline=False
            )

            em.add_field(
                name="Before",
                value=f"`{after.region}`",
                inline=False
            )

            await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        em = discord.Embed(
            title="New Role Created!",
            timestamp=datetime.utcnow(),
            color=discord.Colour.blue()
        )

        em.add_field(
            name="Role",
            value=f"{role.mention}",
            inline=False
        )

        await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        em = discord.Embed(
            title="Role Deleted!",
            timestamp=datetime.utcnow(),
            color=discord.Colour.blue()
        )

        em.add_field(
            name = "Role",
            value = f"`@ {role.name}`",
            inline=False
        )

        await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if before.name != after.name:
            em = discord.Embed(
                title="Role Name Updated!",
                timestamp=datetime.utcnow(),
                color=discord.Colour.blue()
            )

            em.add_field(
                name = "Before",
                value = f"`{before.name}`",
                inline=False
            )

            em.add_field(
                name = "After",
                value = f"`{after.name}`",
                inline=False
            )

            await self.log_channel.send(embed=em)

        if before.colour != after.colour:
            em = discord.Embed(
                title = "Role Colour Changed!",
                timestamp=datetime.utcnow(),
                color=discord.Colour.blue()
            )

            em.add_field(
                name="Before",
                value=f"`#{before.colour}`",
                inline=False
            )

            em.add_field(
                name="After",
                value=f"`#{after.colour}`",
                inline=False
            )

            await self.log_channel.send(embed=em)

        if before.permissions != after.permissions:
            em = discord.Embed(
                title = "Role Permissions Updated!",
                timestamp = datetime.utcnow(),
                color = discord.Colour.blue()
            )

            em.add_field(
                name="Role",
                value=f"`{after.name}`",
                inline = False
            )

            await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        em = discord.Embed(
            title = "Server Channel Created!",
            timestamp = datetime.utcnow(),
            color = discord.Colour.blue()
        )

        em.add_field(
            name = "Channel",
            value = f"{channel.mention}",
            inline = False
        )

        em.add_field(
            name = "Category",
            value = f"`{channel.category}`",
            inline = False
        )

        await self.log_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        em = discord.Embed(
            title = "Server Channel Deleted!",
            timestamp = datetime.utcnow(),
            color = discord.Colour.blue()
        )

        em.add_field(
            name = "Channel",
            value = f"`#{channel.name}`",
            inline = False
        )

        em.add_field(
            name = "Category",
            value = f"`{channel.category}`",
            inline = False
        )

        await self.log_channel.send(embed=em)

def setup(bot):
    bot.add_cog(logging(bot))
    print("( \ ) -- Logging is ready! -- ( / )")
