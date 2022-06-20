import discord
import asyncio
import aiosqlite
from discord import app_commands
from discord.ext import commands

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog: str):

        try:
            if cog == "events":
                cog = "src.events.events"
            if cog == "mod":
                cog = "src.mod.mod"
            if cog == "owner":
                cog = "src.owner.owner"
            if cog == "tickets":
                cog = "src.tickets.tickets"
            if cog == "utils":
                cog = "src.utils.utils"
            await self.bot.unload_extension(cog)
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            a = await ctx.reply('**`SUCCESS`**')
            await asyncio.sleep(5)
            await a.delete()
            await ctx.message.delete()
    
    @commands.command(name='delete', hidden=True)
    @commands.is_owner()
    async def delete(self, ctx, database: str):
        confessions = ("confessions", "confessionsdatabase", "confession", "confessiondatabase", "confess", "confessdatabase")
        counting = ("counting", "countingdatabase")
        embed = ("embedchannels", "embed", "embeds", "embeddatabase", "embedsdatabase")
        modlog = ("modlogs", "modlog", "modlogsdatabase", "modlogdatabase")
        suggestions = ("suggestions", "suggestionsdatabase", "suggestion", "suggestiondatabase", "suggest", "suggestdatabase")
        tickets = ("ticket", "tickets", "ticketdatabase", "ticketsdatabase")
        db = await aiosqlite.connect('database.db')
        if any(thing in database for thing in confessions):
            await db.execute('DROP TABLE confessions;')
            await db.commit()
            await db.close()
            a = await ctx.reply('Done!')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await a.delete()
        if any(thing in database for thing in counting):
            await db.execute('DROP TABLE counting;')
            await db.commit()
            await db.close()
            a = await ctx.reply('Done!')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await a.delete()
        if any(thing in database for thing in embed):
            await db.execute('DROP TABLE embedchannels;')
            await db.commit()
            await db.close()
            a = await ctx.reply('Done!')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await a.delete()
        if any(thing in database for thing in modlog):
            await db.execute('DROP TABLE modlogs;')
            await db.commit()
            await db.close()
            a = await ctx.reply('Done!')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await a.delete()
        if any(thing in database for thing in suggestions):
            await db.execute('DROP TABLE suggestions;')
            await db.commit()
            await db.close()
            a = await ctx.reply('Done!')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await a.delete()
        if any(thing in database for thing in tickets):
            await db.execute('DROP TABLE ticketdatabase;')
            await db.commit()
            await db.close()
            a = await ctx.reply('Done!')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await a.delete()
        else:
            a = await ctx.reply(f'**`ERROR:`** No database found!')
            await asyncio.sleep(5)
            await a.delete()
            await ctx.message.delete()
            return

    @commands.command(name='confessionsdatabase', hidden=True)
    @commands.is_owner()
    async def confessionsdatabase(self, ctx):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute("""
            CREATE TABLE confessions (
            guild_id INTEGER,
            channel_id INTEGER,
            counter INTEGER
        )""")
        row = await cursor.fetchone()
        rows = await cursor.fetchall()
        await cursor.close()
        cursor = await db.execute('INSERT INTO confessions VALUES (?,?,?);', (0, 0, 0))
        await db.commit()
        await db.close()
        a = await ctx.reply('Done!')
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()

    @commands.command(name='countingdatabase', hidden=True)
    @commands.is_owner()
    async def countingdatabase(self, ctx):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute("""
            CREATE TABLE counting (
            guild_id INTEGER,
            channel_id INTEGER,
            number INTEGER,
            last_counter INTEGER
        )""")
        row = await cursor.fetchone()
        rows = await cursor.fetchall()
        await cursor.close()
        cursor = await db.execute('INSERT INTO counting VALUES (?,?,?,?);', (0, 0, 0, 0))
        await db.commit()
        await db.close()
        a = await ctx.reply('Done!')
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()

    @commands.command(name='embedchanneldatabase', hidden=True)
    @commands.is_owner()
    async def embedchanneldatabase(self, ctx):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute("""
            CREATE TABLE embedchannels (
            guild_id INTEGER,
            channel_id INTEGER,
            title TEXT,
            footer TEXT
        )""")
        row = await cursor.fetchone()
        rows = await cursor.fetchall()
        await cursor.close()
        cursor = await db.execute('INSERT INTO embedchannels VALUES (?,?,?,?);', (0, 0, 'null', 'null'))
        await db.commit()
        await db.close()
        a = await ctx.reply('Done!')
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()

    @commands.command(name='modlogsdatabase', hidden=True)
    @commands.is_owner()
    async def modlogsdatabase(self, ctx):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute("""
            CREATE TABLE modlogs (
            guild_id INTEGER,
            channel_id INTEGER
        )""")
        row = await cursor.fetchone()
        rows = await cursor.fetchall()
        await cursor.close()
        cursor = await db.execute('INSERT INTO modlogs VALUES (?,?);', (0, 0))
        await db.commit()
        await db.close()
        a = await ctx.reply('Done!')
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()

    @commands.command(name='suggestionsdatabase', hidden=True)
    @commands.is_owner()
    async def suggestionsdatabase(self, ctx):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute("""
            CREATE TABLE suggestions (
            guild_id INTEGER,
            channel_id INTEGER,
            counter INTEGER
        )""")
        row = await cursor.fetchone()
        rows = await cursor.fetchall()
        await cursor.close()
        cursor = await db.execute('INSERT INTO suggestions VALUES (?,?,?);', (0, 0, 0))
        await db.commit()
        await db.close()
        a = await ctx.reply('Done!')
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()

    @commands.command(name='ticketdatabase', hidden=True)
    @commands.is_owner()
    async def ticketdatabase(self, ctx):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute("""
            CREATE TABLE ticketdatabase (
            guild_id INTEGER,
            category_id INTEGER,
            roles STRING,
            counter INTEGER
        )""")
        row = await cursor.fetchone()
        rows = await cursor.fetchall()
        await cursor.close()
        cursor = await db.execute('INSERT INTO ticketdatabase VALUES (?,?,?,?);', (0, 0, 'null', 0))
        await db.commit()
        await db.close()
        a = await ctx.reply('Done!')
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()

    @app_commands.command(description="Ping Command")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('{0} ms'.format(round(self.bot.latency, 1)), ephemeral=True)

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
