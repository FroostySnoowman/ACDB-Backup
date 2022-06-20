import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class SuggestCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suggestions', hidden=True)
    @commands.is_owner()
    async def suggestions(self, ctx):
        await ctx.send(f'Suggestions')

class SuggestionsCog(commands.GroupCog, name="suggestions"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="set", description="Set the suggestions channel!")
    @app_commands.describe(channel="What channel do you want to set as the suggestions channel?")
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from suggestions WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            if interaction.user.guild_permissions.administrator:
                await db.execute('INSERT INTO suggestions VALUES (?,?,?);', (interaction.guild.id, channel.id, 0))
                await interaction.response.send_message(f"I've set the suggestions channel to **{channel}**! To remove this, type `/config modlogs remove`", ephemeral=True)
                await db.commit()
                await db.close()
        else:
            await interaction.response.send_message(f"You already have a suggestions channel set!", ephemeral=True)
            await db.close()

    @app_commands.command(name="remove", description="Remove the suggestions channel!")
    async def modlogs(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from suggestions WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message(f"You can't remove a suggestions channel if you don't have one!", ephemeral=True)
            await db.close()
        else:
            if interaction.user.guild_permissions.administrator:
                await db.execute('DELETE FROM suggestions WHERE guild_id=?', (interaction.guild.id, ))
                await interaction.response.send_message(f"Removed the suggestions channel!", ephemeral=True)
                await db.commit()
                await db.close()
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
                await db.close()

class Suggest(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="suggest", description="Submit a suggestion!")
    @app_commands.describe(suggestion="What is your suggestion?")
    async def suggest(self, interaction: discord.Interaction, suggestion: str) -> None:
        try:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from suggestions WHERE guild_id=?', (interaction.guild.id, ))
            a = await cursor.fetchone()
            await db.execute('UPDATE suggestions SET counter=counter + ? WHERE guild_id=?', (1, interaction.guild.id))
            await db.commit()
            embed = discord.Embed(
                description=
                f"""
{suggestion}
""",
                color=0x00FFD4)
            embed.set_author(name=f"Suggestion #{a[2]} from {interaction.user}", icon_url = interaction.user.display_avatar.url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Submitted at:")
            channel = self.bot.get_channel(a[1])
            suggestionmessage = await channel.send(embed=embed)
            await suggestionmessage.add_reaction('👍')
            await suggestionmessage.add_reaction('👎')
            await interaction.response.send_message(f"Your suggestion has been added to {channel.mention}", ephemeral=True)
            await db.commit()
            await db.close()
        except:
            await interaction.response.send_message(f"This guild doesn't have suggestions setup!", ephemeral=True)
            return

async def setup(bot):
    await bot.add_cog(SuggestCog(bot))
    await bot.add_cog(SuggestionsCog(bot))
    await bot.add_cog(Suggest(bot))
