import discord
import os
import string
import fnmatch
import asyncio
import random

from discord.ext import commands
from captcha.image import ImageCaptcha

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)

        channel_id = payload.channel_id
        channel = self.bot.get_channel(channel_id)

        user_id = payload.user_id
        user = guild.get_member(user_id)

        message_id = payload.message_id
        message = await channel.fetch_message(message_id)
        
        emoji = payload.emoji.name
        
        if channel_id == 833401618564251699 and emoji == "✅":
            if not user.bot:
                await message.remove_reaction('✅', user)
                
                try:
                    await user.send("This is a test message in-order to check if the bot can actually DM you! Please ignore this!", delete_after=3.0)
                    
                except:
                    return
                
                image = ImageCaptcha(width = 280, height = 90)
                    
                ranStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                image.write(f'{ranStr}', f"/home/yamin/Coding/Discord/Discord-PY/AngelicBot/cogs/captchaImgs/captcha{ranStr}.png")
                
                em = discord.Embed(
                    title = "Verification Message!",
                    description = "Please write down the combination of words and letters **exactly** how it's shown!",
                    color = discord.Colour.green()
                )
                
                em.set_footer(text="Complete this captcha in-order to verify yourself! You have 15 seconds!")
                file = discord.File(f"/home/yamin/Coding/Discord/Discord-PY/AngelicBot/cogs/captchaImgs/captcha{ranStr}.png", filename="image.png")
                em.set_image(url="attachment://image.png")
                em.set_thumbnail(url=self.bot.user.avatar_url)
                
                await user.send(file=file, embed=em)
                
                if os.path.exists(f'/home/yamin/Coding/Discord/Discord-PY/AngelicBot/cogs/captchaImgs/captcha{ranStr}.png'):
                    os.remove(f"/home/yamin/Coding/Discord/Discord-PY/AngelicBot/cogs/captchaImgs/captcha{ranStr}.png")
                
                msg = await self.bot.wait_for('message', check=lambda m: m.author == user and m.channel == user.dm_channel,timeout=15)
                
                if msg.content is None:
                    emb = discord.Embed(
                        title = "Error!",
                        description = "You didn't answer the message in time! Please try again later!",
                        color = discord.Colour.red()
                    )
                    
                    emb.set_footer(text="This is an error message!")
                    
                    await user.send(embed=emb)
                    return
                
                if msg.content != f"{ranStr}":
                    emb = discord.Embed(
                        title = "Error!",
                        description = "You have got the captcha message wrong! Please try again later!",
                        color = discord.Colour.red()
                    )
                    
                    emb.set_footer(text="This is an error message!")
                    
                    await user.send(embed=emb)
                    return
                
                else:
                    role1 = discord.utils.find(lambda r: r.name == '「 ➣ 」 Verified', guild.roles)
                    role2 = discord.utils.find(lambda r: r.name == '「 ➣ 」 User', guild.roles)
                    
                    await user.add_roles(role1)
                    await user.remove_roles(role2)
                    
                    embed = discord.Embed(
                        title = "Successfully Verified!",
                        description = "Please enjoy your stay in **AngelicNodes**!",
                        color = discord.Colour.green()
                    )
                    
                    embed.set_footer(text="You have unlocked most of the channels!")
                    embed.set_thumbnail(url=self.bot.user.avatar_url)
                    
                    await user.send(embed=embed)
                    return
    
    @commands.command()
    async def verify(self, ctx):
        role = discord.utils.find(lambda r: r.name == "╸╸╸ 「 Executive 」 ╺╺╺", ctx.guild.roles)

        if role in ctx.author.roles:        
            em = discord.Embed(
                    title = "Verification",
                    description = "You will need to verify whether you are a bot/alt account by using our captcha system!",
                    color = discord.Colour.blue()
                )
                
            em.set_footer(text="Verify yourself in-order to gain access to the server!")
            em.set_thumbnail(url=self.bot.user.avatar_url)
                
            em.add_field(
                    name = "Step 1",
                    value = "React to this message with a ✅ emoji!",
                    inline = False
                )
                
            em.add_field(
                    name = "Step 2",
                    value = "Please check your DMs for any message. (Please make sure your DMs are on, otherwise this will not work!)",
                    inline = False 
                )
                
            em.add_field(
                    name = "Step 3",
                    value = "Once you've completed the captcha, you should have access to the server!",
                    inline = False
                )
                
            msg = await ctx.channel.send(embed=em)
            
            await msg.add_reaction('✅')
            return
        
        else:
            return

def setup(bot):
    bot.add_cog(Verify(bot))
    print("( \ ) -- Verify is loaded! -- ( / )")