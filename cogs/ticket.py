import datetime

import chat_exporter
import discord
import asyncio
import numpy as np

import motor.motor_asyncio
import dns
import io

from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

cluster = AsyncIOMotorClient("mongodb://vertoxen:omegamemes567@private-1.arknodes.com:25700/main?authMechanism=DEFAULT&retryWrites=true&w=majority")
injection = AsyncIOMotorClient("mongodb://vertoxen:omegamemes567@private-1.arknodes.com:25700/main?authMechanism=DEFAULT&retryWrites=true&w=majority")

db = cluster['main']
injector = injection['main']
cursor = db['count']
inject = injector['main']

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        self.ticket_post = self.bot.get_channel(833484794108313611)
        self.ticket_log = self.bot.get_channel(833509258331029524)
        chat_exporter.init_exporter(self.bot)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)

        channel_id = payload.channel_id
        channel = self.bot.get_channel(channel_id)

        user_id = payload.user_id
        user = guild.get_member(user_id)

        message_id = payload.message_id
        emoji = payload.emoji.name

        if channel_id == 833484794108313611 and emoji == "🎫":
            if not user.bot:
                results = await inject.find_one({"user_id": user.id})

                if results is not None:
                    em = discord.Embed(
                        title = "Error!",
                        description = "You can only open **1** ticket!",
                        color = discord.Colour.red()
                    )

                    await user.send(embed=em)

                    message = await channel.fetch_message(message_id)
                    await message.remove_reaction(payload.emoji, user)

                    return

                message = await channel.fetch_message(message_id)
                await message.remove_reaction("🎫", user)

                member = discord.utils.find(lambda m: m.id == user.id, guild.members)
                category = discord.utils.get(guild.categories, name="╸╸╸ 「 Tickets 」 ╺╺╺")
                staff = discord.utils.get(guild.roles, name="╸╸╸ 「 Staff 」 ╺╺╺")

                check = await cursor.find_one({"num": 1})

                if check is None:
                    ins = {
                        "num": 1, "count": 1
                    }

                    await cursor.insert_one(ins)

                num = await cursor.find_one({"num": 1})

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    staff: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }

                await category.create_text_channel(f"「➵」-ticket-{num['count']}", overwrites=overwrites)
                ticket_channel_name = discord.utils.get(guild.channels, name=f"「➵」-ticket-{num['count']}")
                ticket_channel_id = ticket_channel_name.id
                ticket_channel = self.bot.get_channel(ticket_channel_id)

                newNum = num['count'] + 1

                await cursor.update_one({"num": 1}, {"$set": {"count": newNum}})

                ins = {
                    "ticket": num['count'], "channel_name": ticket_channel_name.name, "channel_id": ticket_channel_name.id,
                    "user_id": user_id, "guild_id": guild.id, "isClaimed": "False"
                }

                await inject.insert_one(ins)

                em = discord.Embed(
                    title = "How can we help you today?",
                    color = discord.Colour.blue()
                )

                em.add_field(
                    name = "User",
                    value = f"|| {user.mention} ||"
                )

                em.add_field(
                    name = "✅ Claim the ticket!",
                    value = "```Claim the ticket so that the other staff members know that the ticket is already being supported.```",
                    inline = False
                )

                em.add_field(
                    name = "🎫 Save a transcript!",
                    value = "```Save a transcript as a way to back up all of the messages.```",
                    inline = False
                )

                em.add_field(
                    name="❌ Close the Ticket!",
                    value="```Close the ticket as soon as the problem has been resolved.```",
                    inline=False
                )

                ticket_channel_message = await ticket_channel.send(embed=em)

                await ticket_channel_message.add_reaction('✅')
                await ticket_channel_message.add_reaction('🎫')
                await ticket_channel_message.add_reaction('❌')

                await ticket_channel.send(f"{user.mention} <@&833137447377960990>", delete_after=1.0)

        db_ticket = inject.find({"guild_id": guild.id})

        db_ticket_channel_id = []

        async for db_ticket_id in db_ticket:
            db_ticket_channel_id.append(db_ticket_id['channel_id'])

        if channel.id in db_ticket_channel_id and emoji == '✅' and user.bot == False:
            db_channel = await inject.find_one({"channel_id": channel_id})
            db_check = db_channel['isClaimed']
            db_channel_name = db_channel['channel_name']
            db_channel_user_id = db_channel['user_id']
            db_channel_user = self.bot.get_user(db_channel_user_id)

            message = await channel.fetch_message(message_id)
            await message.remove_reaction(payload.emoji, user)

            staff = discord.utils.get(guild.roles, name="╸╸╸ 「 Staff 」 ╺╺╺")

            if staff in user.roles:
                if db_check == "False":
                    member = discord.utils.find(lambda m: m.id == user.id, guild.members)
                    category = discord.utils.get(guild.categories, name="╸╸╸ 「 Tickets 」 ╺╺╺")
                    staff = discord.utils.get(guild.roles, name="╸╸╸ 「 Staff 」 ╺╺╺")
                    needer = guild.get_member(db_channel_user_id)

                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                        staff: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                        needer: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    }

                    await channel.edit(overwrites=overwrites)

                    emb = discord.Embed(
                        title = "Claimed!",
                        description = "A staff member has claimed the ticket",
                        color = discord.Colour.blue()
                    )

                    emb.add_field(
                        name = "Staff Member",
                        value = f"`{user}`",
                        inline = False
                    )

                    await channel.send(embed=emb, delete_after=10.0)

                    await inject.update_one({"channel_id": channel.id}, {"$set": {"isClaimed": "True"}})
                    return

                else:
                    em = discord.Embed(
                        title = "Error!",
                        description = f"**{user}**, this ticket is already claimed!",
                        color = discord.Colour.red()
                    )

                    await channel.send(embed=em)
                    return

            else:
                em = discord.Embed(
                    title = "Error!",
                    description = "A staff member must claim the ticket!",
                    color = discord.Colour.red()
                )

                await channel.send(embed=em)
                return

        if channel.id in db_ticket_channel_id and emoji == '❌' and user.bot == False:
            db_channel = await inject.find_one({"channel_id": channel_id})
            db_channel_name = db_channel['channel_name']
            db_channel_user_id = db_channel['user_id']
            db_channel_user = self.bot.get_user(db_channel_user_id)

            message = await channel.fetch_message(message_id)
            await message.remove_reaction(payload.emoji, user)

            em = discord.Embed(
                title = "Ticket Closed!",
                description = "Ticket will be deleted in `10 seconds`!",
                color = discord.Colour.blue()
            )

            em.add_field(
                name = "Details",
                value = f"**Ticket Opened By:** {db_channel_user.mention}\n**Ticket Closed By:** {user.mention}",
                inline = False
            )

            await channel.send(embed=em)
            await asyncio.sleep(10)
            await channel.delete()

            emLog = discord.Embed(
                title = "Closed Ticket",
                description = f"**{db_channel_name}** was just closed by **{user}**!",
                timestamp = datetime.datetime.utcnow(),
                color = discord.Colour.blue()
            )

            await self.ticket_log.send(embed=emLog)

            await inject.delete_one({"channel_id": channel.id})
            return

        if channel.id in db_ticket_channel_id and emoji == '🎫' and user.bot == False:
            staff = discord.utils.get(guild.roles, name="╸╸╸ 「 Staff 」 ╺╺╺")

            if staff in user.roles:
                transcript = await chat_exporter.export(channel)
                transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{channel.name}.html")

                emSend = discord.Embed(
                    title = "Transcript Sent!",
                    description = "A transcript has been saved!",
                    color = discord.Colour.blue()
                )

                await channel.send(embed=emSend)

                emTranscript = discord.Embed(
                    title = "New Transcript",
                    description = f"Transcript from **{channel.name}**!",
                    timestamp = datetime.datetime.utcnow(),
                    color = discord.Colour.blue()
                )

                await self.ticket_log.send(embed=emTranscript, file=transcript_file)
                message = await channel.fetch_message(message_id)
                await message.remove_reaction(payload.emoji, user)
                return

            else:
                emError = discord.Embed(
                    title = "Error!",
                    description = "Only staff can save a transcript!",
                    color = discord.Colour.red()
                )

                await channel.send(embed=emError)

                message = await channel.fetch_message(message_id)
                await message.remove_reaction(payload.emoji, user)

    @commands.command()
    async def post(self, ctx):
        em = discord.Embed(
            title = "Ticket Support",
            color = discord.Colour.blue()
        )

        em.add_field(
            name = "Before Creating Ticket!",
            value = "```Please create a ticket only if you think it's crucial! This cannot be stressed enough due to the existence of the community-support channel! So just beware, creating an unnecessary ticket will lead to a warning!```",
            inline = False
        )

        em.add_field(
            name = "Creating Ticket!",
            value = "React to this message with a :ticket:",
            inline = False
        )

        em.set_footer(text="Please create a ticket for important issues only!")

        msg = await self.ticket_post.send(embed=em)
        await msg.add_reaction("🎫")

def setup(bot):
    bot.add_cog(Ticket(bot))
    print("( \ ) -- Ticket is loaded! -- ( / )")