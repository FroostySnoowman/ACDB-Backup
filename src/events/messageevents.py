import discord
import aiosqlite
from discord.ext import commands
from datetime import datetime


class MessageEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='messageevents', hidden=True)
    @commands.is_owner()
    async def messageevents(self, ctx):
        await ctx.send(f'Message Events')

    @commands.Cog.listener('on_message')
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        db = await aiosqlite.connect('database.db')
        try:
            cursor = await db.execute('SELECT * from embedchannels WHERE guild_id=? AND channel_id=?', (message.guild.id, message.channel.id))
            a = await cursor.fetchone()
            if message.channel.id == a[1]:
                if a[2] == 'null':
                    if a[3] != 'null':
                        await message.delete()
                        embed = discord.Embed(
                            title="",
                            description=
                            f"{message.content}")
                        embed.set_author(name=f"{message.author.name}", icon_url = message.author.display_avatar.url)
                        embed.set_footer(text=f"{a[3]}")
                        await message.channel.send(embed=embed)
                    else:
                        await message.delete()
                        embed = discord.Embed(
                            title="",
                            description=
                            f"{message.content}")
                        embed.set_author(name=f"{message.author.name}", icon_url = message.author.display_avatar.url)
                        await message.channel.send(embed=embed)
                if a[2] != 'null':
                    if a[3] != 'null':
                        await message.delete()
                        embed = discord.Embed(
                            title=f"{a[2]}",
                            description=
                            f"{message.content}")
                        embed.set_author(name=f"{message.author.name}", icon_url = message.author.display_avatar.url)
                        embed.set_footer(text=f"{a[3]}")
                        await message.channel.send(embed=embed)
                    else:
                        await message.delete()
                        embed = discord.Embed(
                            title=f"{a[2]}",
                            description=
                            f"{message.content}")
                        embed.set_author(name=f"{message.author.name}", icon_url = message.author.display_avatar.url)
                        await message.channel.send(embed=embed)
        except:
            pass
        try:
            cursor2 = await db.execute('SELECT * from counting WHERE guild_id=? AND channel_id=?', (message.guild.id, message.channel.id))
            b = await cursor2.fetchone()
            if message.channel.id == b[1]:
                n = b[2] + 1
                number = int(n)
                try:
                    m = int(message.content)
                    if number != m:
                        await message.delete()
                    else:
                        if b[3] == message.author.id:
                            await message.delete()
                        else:
                            cursor = await db.execute('UPDATE counting SET number=?, last_counter=? WHERE number=? AND channel_id=?', (number, message.author.id, b[2], message.channel.id))
                            await message.add_reaction('✅')
                except:
                    await message.delete()
                    pass
        except:
            pass
        await db.commit()
        await db.close()

    @commands.Cog.listener('on_message_delete')
    async def onmessagedelete(self, message: discord.Message):
        if message.guild:
            if message.author.bot:
                return
            try:
                if message.attachments:
                    db = await aiosqlite.connect('database.db')
                    cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (message.guild.id, ))
                    a = await cursor.fetchone()
                    embed = discord.Embed(
                        description=
                        f"""
**Message sent by {message.author.mention} deleted in {message.channel.mention}**
{message.content}

**Contained an image**
""",
                        color=0xFF0000)
                    embed.set_author(name=f"{message.author}", icon_url = message.author.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
                else:
                    db = await aiosqlite.connect('database.db')
                    cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (message.guild.id, ))
                    a = await cursor.fetchone()
                    embed = discord.Embed(
                        description=
                        f"""
**Message sent by {message.author.mention} deleted in {message.channel.mention}**
{message.content}
""",
                        color=0xFF0000)
                    embed.set_author(name=f"{message.author}", icon_url = message.author.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
            except:
                pass
        else:
            pass

    @commands.Cog.listener('on_message_edit')
    async def onmessage(self, before, after):
        if before.guild:
            if before.author.bot:
                return
            try:
                if after.attachments:
                    if before.content == '':
                        db = await aiosqlite.connect('database.db')
                        cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                        a = await cursor.fetchone()
                        embed = discord.Embed(
                            description=
                            f"""
**Message edited in {before.channel.mention}** [Jump To Message]({before.jump_url})

**After**
{after.content}

**Image**
{after.attachments[0].url}
""",
                            color=0xFF0000)
                        embed.set_author(name=f"{before.author}", icon_url = before.author.display_avatar.url)
                        embed.timestamp=datetime.now()
                        embed.set_footer(text=f"Author: {before.author.id} | Message ID: {before.id}")
                        channel = self.bot.get_channel(a[1])
                        await channel.send(embed=embed)
                        await db.close()
                        return
                    else:
                        db = await aiosqlite.connect('database.db')
                        cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                        a = await cursor.fetchone()
                        embed = discord.Embed(
                            description=
                            f"""
**Message edited in {before.channel.mention}** [Jump To Message]({before.jump_url})

**Before**
{before.content}
**After**
{after.content}

**Image**
{after.attachments[0].url}
""",
                            color=0xFF0000)
                        embed.set_author(name=f"{before.author}", icon_url = before.author.display_avatar.url)
                        embed.timestamp=datetime.now()
                        embed.set_footer(text=f"Author: {before.author.id} | Message ID: {before.id}")
                        channel = self.bot.get_channel(a[1])
                        await channel.send(embed=embed)
                        await db.close()
                        return
                else:
                    db = await aiosqlite.connect('database.db')
                    cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                    a = await cursor.fetchone()
                    embed = discord.Embed(
                        description=
                        f"""
**Message edited in {before.channel.mention}** [Jump To Message]({before.jump_url})

**Before**
{before.content}
**After**
{after.content}
""",
                        color=0xFF0000)
                    embed.set_author(name=f"{before.author}", icon_url = before.author.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Author: {before.author.id} | Message ID: {before.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
            except:
                pass
        else:
            pass

async def setup(bot):
    await bot.add_cog(MessageEventsCog(bot))
