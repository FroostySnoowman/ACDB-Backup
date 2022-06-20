import discord
import random
import json
import datetime as DT
import asyncio
import re
import pytz
import aiosqlite
import logging

from discord import Client, app_commands, utils
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.errors import BadArgument
from typing import Counter, Union, Optional

intents = discord.Intents.all()
intents.message_content = True

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Test', style=discord.ButtonStyle.green, custom_id='test')
    async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
       await interaction.response.send_message('pp', ephemeral=True)

playing = discord.Game(name="Developing...")
class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), owner_id=503641822141349888, intents=intents, activity=playing, status=discord.Status.dnd)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(PersistentView())
            self.persistent_views_added = True

        await self.tree.sync()
        
        print(f'Signed in as {self.user}')

client = PersistentViewBot()

initial_extensions = ['src.events.botevents',
                      'src.events.channelevents',
                      'src.events.memberevents',
                      'src.events.messageevents',
                      'src.events.roleevents',
                      'src.events.voiceevents',
                      'src.mod.mod',
                      'src.owner.owner',
                      'src.tickets.tickets',
                      'src.utils.confessions',
                      'src.utils.suggestions',
                      'src.utils.utils']

async def load_extensions():
    for extension in initial_extensions:
        await client.load_extension(extension)

async def main():
    async with client:
        await load_extensions()
        await client.start('')

logging.basicConfig(level=logging.INFO)

asyncio.run(main())
