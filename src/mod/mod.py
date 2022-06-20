import discord
import asyncio
from discord import app_commands
from discord.ext import commands


class ModCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mod', hidden=True)
    @commands.is_owner()
    async def mod(self, ctx):
        await ctx.send(f'Mod')

    @app_commands.command(description="Purge Command")
    @app_commands.describe(number="How many messages do you want to delete?")
    async def purge(self, interaction: discord.Interaction, number: int):
        if interaction.user.guild_permissions.administrator:
            await interaction.channel.purge(limit=number+1)
            await interaction.response.send_message(f"Cleared By: {interaction.user.mention}")
            a = await interaction.original_message()
            await asyncio.sleep(2)
            await a.delete()
            return
        else:
            await interaction.response.send_message("You do not have permission to use this command!")
            a = await interaction.original_message()
            await asyncio.sleep(5)
            await a.delete()

async def setup(bot):
    await bot.add_cog(ModCog(bot))
