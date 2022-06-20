import discord
import aiosqlite
from discord.ext import commands
from datetime import datetime


class ChannelEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='channelevents', hidden=True)
    @commands.is_owner()
    async def channelevents(self, ctx):
        await ctx.send(f'Channel Events')

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            if isinstance(channel, discord.CategoryChannel):
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (channel.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=0xFF0000)
                if channel.guild.icon is None:
                    selfavatar = await channel.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Category Channel Created", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Category Channel Created", icon_url = channel.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
            if isinstance(channel, discord.VoiceChannel):
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (channel.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{channel.mention}
""",
                    color=0xFF0000)
                if channel.guild.icon is None:
                    selfavatar = await channel.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Voice Channel Created", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Voice Channel Created", icon_url = channel.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
            if isinstance(channel, discord.TextChannel):
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (channel.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{channel.mention}
""",
                    color=0xFF0000)
                if channel.guild.icon is None:
                    selfavatar = await channel.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Text Channel Created", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Text Channel Created", icon_url = channel.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            if isinstance(channel, discord.CategoryChannel):
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (channel.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=0xFF0000)
                if channel.guild.icon is None:
                    selfavatar = await channel.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Category Channel Deleted", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Category Channel Deleted", icon_url = channel.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
            if isinstance(channel, discord.VoiceChannel):
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (channel.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=0xFF0000)
                if channel.guild.icon is None:
                    selfavatar = await channel.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Voice Channel Deleted", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Voice Channel Deleted", icon_url = channel.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
            if isinstance(channel, discord.TextChannel):
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (channel.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=0xFF0000)
                if channel.guild.icon is None:
                    selfavatar = await channel.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Text Channel Deleted", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Text Channel Deleted", icon_url = channel.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        try:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
            a = await cursor.fetchone()
            if before.name != after.name:
                embed = discord.Embed(
                    description=
                    f"""

**{before.mention} name updated!**

**Before**:
{before.name}

**After**:
{after.name}
""",
                    color=0xFF0000)
                if before.guild.icon is None:
                    selfavatar = await before.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"{before.guild.name}", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"{before.guild.name}", icon_url = before.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {before.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
            await db.close()
        except:
            pass

async def setup(bot):
    await bot.add_cog(ChannelEventsCog(bot))
