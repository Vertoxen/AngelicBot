import discord
import asyncio

from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.ticket_post = self.bot.get_channel(833484794108313611)

    @commands.command()
    async def post(self, ctx):
        em = discord.Embed(
            title = "Ticket Support",
            description = "Please react with :ticket: to create a ticket!",
            color = discord.Colour.blue()
        )

        em.set_footer(text="Please create a ticket if you think it's important only!")

        await self.ticket_post.send(embed=em)

        

def setup(bot):
    bot.add_cog(Ticket(bot))
    print("( \ ) -- Ticket is loaded! -- ( / )")