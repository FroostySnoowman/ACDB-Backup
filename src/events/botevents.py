import discord
from discord.ext import commands


class BotEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='botevents', hidden=True)
    @commands.is_owner()
    async def botevents(self, ctx):
        await ctx.send(f'Bot Events')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        bot_add = guild.audit_logs(action=discord.AuditLogAction.bot_add)
        embed = discord.Embed(
            title="Thank you!",
            description=
            f"""
Thank you for inviting me to the server!

To get started, use `/config` to view the configuration options!
""",
            color=0x00FFE8)
        async for entry in bot_add:
            await entry.user.send(embed=embed)
            return

async def setup(bot):
    await bot.add_cog(BotEventsCog(bot))
