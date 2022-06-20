import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands
from typing import Optional

class UtilsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='utils', hidden=True)
    @commands.is_owner()
    async def utils(self, ctx):
        await ctx.send(f'Utils')

class CountingCog(commands.GroupCog, name="counting"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 
    
    channel = app_commands.Group(name="channel", description="Add/remove a counting channel!")

    @channel.command(name="set", description="Set the counting channel!")
    @app_commands.describe(channel="What channel do you want to set as the counting channel?")
    async def set(self, interaction: discord.Interaction, channel: discord.TextChannel):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from counting WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            if interaction.user.guild_permissions.administrator:
                await db.execute('INSERT INTO counting VALUES (?,?,?,?);', (interaction.guild.id, channel.id, 0, 0))
                await interaction.response.send_message(f"I've set the counting channel to **{channel}**! To remove this, type `/counting channel remove`", ephemeral=True)
                await db.commit()
                await db.close()
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
                await db.close()
        else:
            await interaction.response.send_message(f"You already have a counting channel set!", ephemeral=True)
            await db.close()

    @channel.command(name="remove", description="Remove the counting channel!")
    async def remove(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from counting WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message(f"You can't remove a counting channel if you don't have one!", ephemeral=True)
            await db.close()
        else:
            if interaction.user.guild_permissions.administrator:
                await db.execute('DELETE FROM counting WHERE guild_id=?', (interaction.guild.id, ))
                await interaction.response.send_message(f"Removed the counting channel!", ephemeral=True)
                await db.commit()
                await db.close()
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
                await db.close()

class EmbedChannelCog(commands.GroupCog, name="embedchannel"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="add", description="Make an embed channel!")
    @app_commands.describe(channel="What channel do you want to set as an embed channel?")
    @app_commands.describe(title="Set a title to your embed! (Max x characters)")
    @app_commands.describe(footer_message="Set a footer message! (Max x characters)")
    async def add(self, interaction: discord.Interaction, channel: discord.TextChannel, title: Optional[str], footer_message: Optional[str]):
        db = await aiosqlite.connect('database.db')
        try:
            cursor = await db.execute('SELECT * from embedchannels WHERE channel_id=?', (channel.id, ))
            a = await cursor.fetchone()
            b = a[1]
            await interaction.response.send_message(f"You can't set this channel as an embed channel twice! Try removing it.", ephemeral=True)
            await db.close()
            return
        except:
            if title is None:
                if footer_message is None:
                    await db.execute('INSERT INTO embedchannels VALUES (?,?,?,?);', (interaction.guild.id, channel.id, 'null', 'null'))
                    await db.commit()
                    await db.close()
                    await interaction.response.send_message(f"I've set {channel.mention} to be an embed channel with no title or footer message!", ephemeral=True)
                    return
                else:
                    if len(footer_message) > 250:
                        await interaction.response.send_message("You can only have a maximum of 250 characters in a footer!", ephemeral=True)
                        await db.close()
                        return
                    else:
                        await db.execute('INSERT INTO embedchannels VALUES (?,?,?,?);', (interaction.guild.id, channel.id, 'null', f'{footer_message}'))
                        await db.commit()
                        await db.close()
                        await interaction.response.send_message(f"I've set {channel.mention} to be an embed channel with no title and a footer message of `{footer_message}`!", ephemeral=True)
                        return
            else:
                if footer_message is None:
                    await db.execute('INSERT INTO embedchannels VALUES (?,?,?,?);', (interaction.guild.id, channel.id, f'{title}', 'null'))
                    await db.commit()
                    await db.close()
                    await interaction.response.send_message(f"I've set {channel.mention} to be an embed channel with a title of `{title}` and no footer message.", ephemeral=True)
                    return
                else:
                    if len(footer_message) > 250:
                        await interaction.response.send_message(f"You can only have a maximum of 250 characters in a footer!", ephemeral=True)
                        await db.close()
                        return
                    else:
                        if len(title) > 250:
                            await interaction.response.send_message(f"You can only have a maximum of 250 characters in a title!", ephemeral=True)
                            await db.close()
                            return
                        else:
                            await db.execute('INSERT INTO embedchannels VALUES (?,?,?,?);', (interaction.guild.id, channel.id, f'{title}', f'{footer_message}'))
                            await db.commit()
                            await db.close()
                            await interaction.response.send_message(f"I've set {channel.mention} to be an embed channel with a title of `{title}` and a footer message of `{footer_message}`!", ephemeral=True)
                            return

    @app_commands.command(name="remove", description="Remove an embed channel!")
    @app_commands.describe(channel="What channel do you want to remove as an embed channel?")
    async def remove(self, interaction: discord.Interaction, channel: discord.TextChannel):
        db = await aiosqlite.connect('database.db')
        try:
            cursor = await db.execute('SELECT * from embedchannels WHERE channel_id=?', (channel.id, ))
            a = await cursor.fetchone()
            if a[1] is None:
                await interaction.response.send_message(f"That channel doesn't appear to be within the list. Please be assure that {channel.mention} has been configured.", ephemeral=True)
            else:
                await db.execute('DELETE FROM embedchannels WHERE channel_id=?', (channel.id, ))
                await interaction.response.send_message(f"I've removed {channel.mention} from the embed channel list.", ephemeral=True)
        except:
            await interaction.response.send_message(f"That channel doesn't appear to be within the list. Please be assure that {channel.mention} has been configured.", ephemeral=True)
        await db.commit()
        await db.close()

class TicketCog(commands.GroupCog, name="tickets"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 
    
    config = app_commands.Group(name="config", description="Configure your ticket system!")

    @config.command(name="set", description="Setup your support tickets!")
    @app_commands.describe(category_channel="What category do you want the tickets to go to?")
    @app_commands.describe(role1="What roles do you want to have access to your tickets?")
    async def set(self, interaction: discord.Interaction, category_channel: discord.CategoryChannel, role1: discord.Role, role2: Optional[discord.Role], role3: Optional[discord.Role], role4: Optional[discord.Role], role5: Optional[discord.Role]):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from ticketdatabase WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            if interaction.user.guild_permissions.administrator:
                d = [r.id for r in [role1, role2, role3, role4, role5] if r]
                await db.execute('INSERT INTO ticketdatabase VALUES (?,?,?,?);', (interaction.guild.id, category_channel.id, f"{d}", 0))
                await db.commit()
                await db.close()
                await interaction.response.send_message(f"You've set `{category_channel}` to recieve your tickets with the role ids of `{d}`!", ephemeral=True)
                return
        else:
            await interaction.response.send_message("You already have a ticket system setup! To remove it, do `/tickets config remove`!", ephemeral=True)

    @config.command(name="remove", description="Remove the ticket system!")
    async def remove(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from ticketdatabase WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message(f"You can't remove the ticket system if you don't have one setup!", ephemeral=True)
            await db.close()
        else:
            if interaction.user.guild_permissions.administrator:
                await db.execute('DELETE FROM ticketdatabase WHERE guild_id=?', (interaction.guild.id, ))
                await interaction.response.send_message(f"Removed the ticket system!", ephemeral=True)
                await db.commit()
                await db.close()
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
                await db.close()

class ModlogCog(commands.GroupCog, name="config"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 
    
    config = app_commands.Group(name="modlogs", description="Configure your modlogs!")

    @config.command(name="channel", description="Set the modlogs channel!")
    @app_commands.describe(channel="What channel do you want to set as the modlogs channel?")
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            if interaction.user.guild_permissions.administrator:
                await db.execute('INSERT INTO modlogs VALUES (?,?);', (interaction.guild.id, channel.id))
                await interaction.response.send_message(f"I've set the modlogs channel to **{channel}**! To remove this, type `/config modlogs remove`", ephemeral=True)
                await db.commit()
                await db.close()
        else:
            await interaction.response.send_message(f"You already have a modlog channel set!", ephemeral=True)
            await db.close()

    @config.command(name="remove", description="Remove the modlogs channel!")
    async def modlogs(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from modlogs WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message(f"You can't remove a modlogs channel if you don't have one!", ephemeral=True)
            await db.close()
        else:
            if interaction.user.guild_permissions.administrator:
                await db.execute('DELETE FROM modlogs WHERE guild_id=?', (interaction.guild.id, ))
                await interaction.response.send_message(f"Removed the modlogs channel!", ephemeral=True)
                await db.commit()
                await db.close()
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
                await db.close()

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))
    await bot.add_cog(CountingCog(bot))
    await bot.add_cog(EmbedChannelCog(bot))
    await bot.add_cog(TicketCog(bot))
    await bot.add_cog(ModlogCog(bot))
