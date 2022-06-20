import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands

class ConfessCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='confessions', hidden=True)
    @commands.is_owner()
    async def confessions(self, ctx):
        await ctx.send(f'Confessions')

class ConfessionsCog(commands.GroupCog, name="confessions"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="set", description="Set the confessions channel!")
    @app_commands.describe(channel="What channel do you want to set as the confessions channel?")
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from confessions WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            if interaction.user.guild_permissions.administrator:
                await db.execute('INSERT INTO confessions VALUES (?,?,?);', (interaction.guild.id, channel.id, 0))
                await interaction.response.send_message(f"I've set the confessions channel to **{channel}**! To remove this, type `/config modlogs remove`", ephemeral=True)
                await db.commit()
                await db.close()
        else:
            await interaction.response.send_message(f"You already have a confessions channel set!", ephemeral=True)
            await db.close()

    @app_commands.command(name="remove", description="Remove the confessions channel!")
    async def modlogs(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from confessions WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message(f"You can't remove a confessions channel if you don't have one!", ephemeral=True)
            await db.close()
        else:
            if interaction.user.guild_permissions.administrator:
                await db.execute('DELETE FROM confessions WHERE guild_id=?', (interaction.guild.id, ))
                await interaction.response.send_message(f"Removed the confessions channel!", ephemeral=True)
                await db.commit()
                await db.close()
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
                await db.close()

class Confess(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="confess", description="Submit a confession!")
    @app_commands.describe(confession="What is your confession?")
    async def confess(self, interaction: discord.Interaction, confession: str) -> None:
        try:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from confessions WHERE guild_id=?', (interaction.guild.id, ))
            a = await cursor.fetchone()
            await db.execute('UPDATE confessions SET counter=counter + ? WHERE guild_id=?', (1, interaction.guild.id))
            await db.commit()
            embed = discord.Embed(
                title=f"Anonymous Confession (#{a[2]})",
                description=
                f"""
"{confession}"
""",
                color=0x00FFD4)
            channel = self.bot.get_channel(a[1])
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Your confession has been added to {channel.mention}", ephemeral=True)
            await db.commit()
            await db.close()
        except:
            await interaction.response.send_message(f"This guild doesn't have confessions setup!", ephemeral=True)
            return

async def setup(bot):
    await bot.add_cog(ConfessCog(bot))
    await bot.add_cog(ConfessionsCog(bot))
    await bot.add_cog(Confess(bot))
