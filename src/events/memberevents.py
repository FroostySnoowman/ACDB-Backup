import discord
import aiosqlite
import asyncio
from discord.ext import commands
from datetime import datetime


class MemberEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='memberevents', hidden=True)
    @commands.is_owner()
    async def memberevents(self, ctx):
        await ctx.send(f'Member Events')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if before.name != after.name:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
**{before.mention} name changed

**Before**
{before.name}
**After**
{after.name}
""",
                    color=0xFF0000)
                embed.set_author(name=f"{before}", icon_url = before.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {before.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
        except:
            pass
        try:
            if before.nick != after.nick:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                a = await cursor.fetchone()
                embed = discord.Embed(
                    description=
                    f"""
**{before.mention} nickname changed**

**Before**
{before.nick}
**After**
{after.nick}
""",
                    color=0xFF0000)
                embed.set_author(name=f"{before}", icon_url = before.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {before.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
        except:
            pass
        try:
            if before.roles != after.roles:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (before.guild.id, ))
                a = await cursor.fetchone()
                before_set = set(before.roles)
                after_set = set(after.roles)
                added_roles = after_set - before_set
                removed_roles = before_set - after_set
                added = ' \n➕ '.join(role.mention for role in added_roles)
                removed = ' \n➖ '.join(role.mention for role in removed_roles)

                if added == '':
                    embed = discord.Embed(
                        description=
                        f"""

**{before.mention} roles removed!**

➖ {removed}
""",
                        color=0xFF0000)
                    embed.set_author(name=f"{before}", icon_url = before.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Member: {before.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
                if removed == '':
                    embed = discord.Embed(
                        description=
                        f"""

**{before.mention} roles added!**

➕ {added}
""",
                        color=0xFF0000)
                    embed.set_author(name=f"{before}", icon_url = before.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Member: {before.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
                else:
                    embed = discord.Embed(
                        description=
                        f"""

**{before.mention} roles changed!**

➕ {added}
➖ {removed}
""",
                        color=0xFF0000)
                    embed.set_author(name=f"{before}", icon_url = before.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Member: {before.id}")
                    channel = self.bot.get_channel(a[1])
                    await channel.send(embed=embed)
                    await db.close()
                    return
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        try:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (member.guild.id, ))
            a = await cursor.fetchone()
            created = member.created_at.timestamp()
            member_created = int(created)
            embed = discord.Embed(
                description=
                f"""
{member.mention} {member}

**Account Created**
<t:{member_created}:R>
""",
                color=0xFF0000)
            embed.set_author(name=f"Member Joined", icon_url = member.display_avatar.url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Member: {member.id}")
            channel = self.bot.get_channel(a[1])
            await channel.send(embed=embed)
            await db.close()
        except:
            pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await asyncio.sleep(5)
        try:
            entries = [
                entry
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban)
            ]
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (guild.id, ))
            a = await cursor.fetchone()
            embed = discord.Embed(
                description=
                f"""
{user.mention} ({user}) was unbanned by {entries[0].user}
""",
                color=0xFF0000)
            embed.set_author(name=f"Member Unbanned", icon_url = user.display_avatar.url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Member: {user.id}")
            channel = self.bot.get_channel(a[1])
            await channel.send(embed=embed)
            await db.close()
            return
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return
        await asyncio.sleep(5)
        try:
            entries = [
                entry
                async for entry in member.guild.audit_logs(limit=1)
                if entry.action in (discord.AuditLogAction.kick, discord.AuditLogAction.ban)
                and entry.target.id == member.id
            ]
            if entries == []:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (member.guild.id, ))
                a = await cursor.fetchone()
                role = ', '.join(x.name for x in member.roles) 
                embed = discord.Embed(
                    description=
                    f"""
{member.mention} {member}

**Roles**
{role}
""",
                    color=0xFF0000)
                embed.set_author(name=f"Member Left", icon_url = member.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {member.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
            if entries[0].action == discord.AuditLogAction.kick:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (member.guild.id, ))
                a = await cursor.fetchone()
                role = ', '.join(x.name for x in member.roles) 
                embed = discord.Embed(
                    description=
                    f"""
{member.mention} ({member}) was kicked by {entries[0].user}

**Roles**
{role}
""",
                    color=0xFF0000)
                embed.set_author(name=f"Member Kicked", icon_url = member.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {member.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
            if entries[0].action == discord.AuditLogAction.ban:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (member.guild.id, ))
                a = await cursor.fetchone()
                role = ', '.join(x.name for x in member.roles) 
                embed = discord.Embed(
                    description=
                    f"""
{member.mention} ({member}) was banned by {entries[0].user}

**Roles**
{role}
""",
                    color=0xFF0000)
                embed.set_author(name=f"Member Banned", icon_url = member.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {member.id}")
                channel = self.bot.get_channel(a[1])
                await channel.send(embed=embed)
                await db.close()
                return
        except:
            pass

async def setup(bot):
    await bot.add_cog(MemberEventsCog(bot))
