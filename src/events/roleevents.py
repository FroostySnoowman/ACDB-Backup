import discord
import aiosqlite
from discord.ext import commands
from datetime import datetime


class RoleEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roleevents', hidden=True)
    @commands.is_owner()
    async def roleevents(self, ctx):
        await ctx.send(f'Role Events')

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        try:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (role.guild.id, ))
            a = await cursor.fetchone()
            embed = discord.Embed(
                description=
                f"""
{role.mention} ({role.name})
""",
                color=0xFF0000)
            if role.guild.icon is None:
                selfavatar = await role.guild.fetch_member(984702871662628948)
                embed.set_author(name=f"Role Created", icon_url = selfavatar.display_avatar.url)
            else:
                embed.set_author(name=f"Role Created", icon_url = role.guild.icon_url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Role: {role.id}")
            channel = self.bot.get_channel(a[1])
            await channel.send(embed=embed)
            await db.close()
            return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        try:
            if before.name != after.name:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
**Before**
{before.name}

**After**
{after.name}
""",
                    color=0xFF0000)
                if before.guild.icon is None:
                    selfavatar = await before.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Role Name Updated", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Role Name Updated", icon_url = before.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Role: {before.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return

            list1 = []
            list2 = []
            if before.permissions != after.permissions:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                a = await cursor.fetchone()
                diff = set(after.permissions).difference(set(before.permissions))
                for perm, value in diff:
                    if value == True:
                        list1.append(perm)
                    else:
                        list2.append(perm)
                added = ' \n➕ '.join(list1)
                removed = '\n➖ '.join(list2)
                if added == '':
                    embed = discord.Embed(
                        description=
                        f"""

**Removed**
➖ {removed}
""",
                        color=0xFF0000)
                    if before.guild.icon is None:
                        selfavatar = await before.guild.fetch_member(984702871662628948)
                        embed.set_author(name=f"Role Permissions Updated", icon_url = selfavatar.display_avatar.url)
                    else:
                        embed.set_author(name=f"Role Permissions Updated", icon_url = before.guild.icon_url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Role: {before.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
                if removed == '':
                    embed = discord.Embed(
                        description=
                        f"""

**Added**
➖ {added}
""",
                        color=0xFF0000)
                    if before.guild.icon is None:
                        selfavatar = await before.guild.fetch_member(984702871662628948)
                        embed.set_author(name=f"Role Permissions Updated", icon_url = selfavatar.display_avatar.url)
                    else:
                        embed.set_author(name=f"Role Permissions Updated", icon_url = before.guild.icon_url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Role: {before.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
                else:
                    embed = discord.Embed(
                        description=
                        f"""

**Added**
➕ {added}

**Removed**
➖ {removed}
""",
                        color=0xFF0000)
                    if before.guild.icon is None:
                        selfavatar = await before.guild.fetch_member(984702871662628948)
                        embed.set_author(name=f"Role Permissions Updated", icon_url = selfavatar.display_avatar.url)
                    else:
                        embed.set_author(name=f"Role Permissions Updated", icon_url = before.guild.icon_url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Role: {before.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
            if before.color != after.color:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
**Before**
{before.color}

**After**
{after.color}
""",
                    color=0xFF0000)
                if before.guild.icon is None:
                    selfavatar = await before.guild.fetch_member(984702871662628948)
                    embed.set_author(name=f"Role Color Updated", icon_url = selfavatar.display_avatar.url)
                else:
                    embed.set_author(name=f"Role Color Updated", icon_url = before.guild.icon_url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Role: {before.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        try:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (role.guild.id, ))
            a = await cursor.fetchone()
            embed = discord.Embed(
                description=
                f"""
{role.name}
""",
                color=0xFF0000)
            if role.guild.icon is None:
                selfavatar = await role.guild.fetch_member(984702871662628948)
                embed.set_author(name=f"Role Deleted", icon_url = selfavatar.display_avatar.url)
            else:
                embed.set_author(name=f"Role Deleted", icon_url = role.guild.icon_url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Role: {role.id}")
            channel = self.bot.get_channel(a[1])
            await channel.send(embed=embed)
            await db.close()
            return
        except:
            pass

async def setup(bot):
    await bot.add_cog(RoleEventsCog(bot))
