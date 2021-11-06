import discord
import datetime
import asyncio
from discord.embeds import Embed
import motor.motor_asyncio

from discord.ext import commands
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

FOOTER = "a-help | AngelicNodes"

cluster = AsyncIOMotorClient("mongodb://vertoxen:omegamemes567@private-1.arknodes.com:25700/main?authMechanism=DEFAULT&retryWrites=true&w=majority")
counter = AsyncIOMotorClient("mongodb://vertoxen:omegamemes567@private-1.arknodes.com:25700/main?authMechanism=DEFAULT&retryWrites=true&w=majority")

db = cluster['main']
cdb = counter['main']

cursor = db['apply']
count = cdb['applyCount']

class Apply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.toggle = []
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(833507916321259525)
        
        check = await count.find_one({"id": 1})
        
        if check is None:
            ins = {"id": 1, count: 0}
            
            await count.insert_one(ins)
        
    @commands.command()
    async def applyToggle(self, ctx):
        role = discord.utils.find(lambda r: r.name == "╸╸╸ 「 Executive 」 ╺╺╺", ctx.guild.roles)

        if role in ctx.author.roles:
            if "True" in self.toggle:
                self.toggle.remove("True")
                self.toggle.append("False")
                
                em = discord.Embed(
                    title = "Staff Application",
                    description = "Staff Applications have now been toggled off!",
                    color = discord.Colour.red()
                )
                
                em.set_footer(text=FOOTER)
                
                await ctx.send(embed=em)
                return
            
            if "False" in self.toggle:
                self.toggle.remove("False")
                self.toggle.append("True")
                
                em = discord.Embed(
                    title = "Staff Application",
                    description = "Staff Applications have now been toggled on!",
                    color = discord.Colour.red()
                )
                
                em.set_footer(text=FOOTER)
                
                await ctx.send(embed=em)
                return
        
        else:
            return
        
    @commands.command()
    async def apply(self, ctx):
        if "True" in self.toggle:
            FOOTER = "a-help | AngelicNodes"
            user = ctx.author
            
            emb = discord.Embed(
                title = "Staff Application",
                description = "Please check your DMs and answer the questions!",
                color = discord.Colour.blue(),
                datetime = datetime.datetime.now(tz=None)
            )
            
            emb.set_footer(text=FOOTER)
            emb.set_thumbnail(url=self.bot.user.avatar_url)
            
            await ctx.message.reply(embed=emb)
            
            try:
                await user.send("This is a test message in-order to check if the bot can actually DM you! Please ignore this!", delete_after=1.0)
                
            except:
                emError = discord.Embed(
                    title = "Error!",
                    description = "The bot could not DM you! Please make sure that your DMs are on!",
                    color = discord.Colour.red()
                )
                
                emError.set_footer(text=FOOTER)
                
                await ctx.message.reply(embed=emError)
                return
            
            FOOTER = "Make sure that your application stays detailed and professional!"
            
            em = discord.Embed(
                name = "Application Started!",
                description = "Your application has started! Please type in `cancel` in-order to cancel the application!",
                color = discord.Colour.blue()
            )
            
            em.set_footer(text=FOOTER)
            em.set_thumbnail(url=self.bot.user.avatar_url)
            
            await user.send(embed=em)
            
            await asyncio.sleep(1)
            
            em1 = discord.Embed(
                title = "Question 1",
                description = "How old are you?",
                color = discord.Colour.blue()
            )
            
            em1.set_footer(text="You have 15 seconds to answer this question!")
            em1.set_thumbnail(url=self.bot.user.avatar_url)
            
            await user.send(embed=em1)
            
            q1 = await self.bot.wait_for('message', check=lambda m: m.author == user and m.channel == user.dm_channel, timeout=15.0)
            
            if q1.content is None:
                embed = discord.Embed(
                    title = "Application Cancelled!",
                    description = "Application cancelled due to **Timeout**!",
                    color = discord.Colour.red()
                )
                
                embed.set_footer(text=FOOTER)
                
                await user.send(embed=embed)
                return
            
            if q1.content.lower() == "cancel":
                embed = discord.Embed(
                    title = "Application Cancelled",
                    description = "The application has been cancelled!",
                    color = discord.Colour.red()
                )
                
                embed.set_footer(text=FOOTER)
                
                await user.send(embed=embed)
                return
            
            else:
                em2 = discord.Embed(
                    title = "Question 2",
                    description = "How many hours can you stay online weekly?",
                    color = discord.Colour.blue()
                )
                
                em2.set_footer(text="You have 15 seconds to answer this question!")
                em2.set_thumbnail(url=self.bot.user.avatar_url)
                
                await user.send(embed=em2)
                
                q2 = await self.bot.wait_for('message', check=lambda m: m.author == user and m.channel == user.dm_channel, timeout=15.0)
                
                if q2.content is None:
                    embed = discord.Embed(
                        title = "Application Cancelled!",
                        description = "Application cancelled due to **Timeout**!",
                        color = discord.Colour.red()
                    )
                    
                    embed.set_footer(text=FOOTER)
                    
                    await user.send(embed=embed)
                    return
                
                if q2.content.lower() == "cancel":
                    embed = discord.Embed(
                        title = "Application Cancelled",
                        description = "The application has been cancelled!",
                        color = discord.Colour.red()
                    )
                    
                    embed.set_footer(text=FOOTER)
                    
                    await user.send(embed=embed)
                    return
                
                else:
                    em3 = discord.Embed(
                        title = "Question 3",
                    )
        
        else:
            em = discord.Embed(
                title = "Error!",
                description = "Staff Applications are currently closed!",
                color = discord.Colour.red()
            )
            
            em.set_footer(text="Please try again once staff applications are announced and open!")
            
            await ctx.send(embed=em)
            return
        
def setup(bot):
    bot.add_cog(Apply(bot))
    print("( \ ) -- Apply is loaded! -- ( / )")