import discord
import aiosqlite
from discord.ext import commands
from datetime import datetime


class VoiceEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='voiceevents', hidden=True)
    @commands.is_owner()
    async def voiceevents(self, ctx):
        await ctx.send(f'Voice Events')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if after.channel and not before.channel:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (member.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{after.channel.name}
""",
                    color=0xFF0000)
                if member.guild.icon is None:
                    selfavatar = await member.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Voice Channel Joined", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Voice Channel Joined", icon_url = member.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {after.channel.id} | Member: {member.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
            if before.channel and not after.channel:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (member.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{before.channel.name}
""",
                    color=0xFF0000)
                if member.guild.icon is None:
                    selfavatar = await member.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Voice Channel Left", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Voice Channel Left", icon_url = member.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {before.channel.id} | Member: {member.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
        except:
            pass

async def setup(bot):
    await bot.add_cog(VoiceEventsCog(bot))
