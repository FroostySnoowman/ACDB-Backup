import discord
import aiosqlite
from discord.ext import commands


class TicketSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
#    @classmethod
#    async def database(cls):
#        self = cls()
#        async with aiosqlite.connect('database.db') as connection:
#            async with connection.execute('SELECT * FROM ticketdatabase WHERE guild_id=?', (984703074650193940, )) as cursor:
#                row = await cursor.fetchone()
#                cls.tickets.label = row[0]
#                return self

    @discord.ui.button(label='d', style=discord.ButtonStyle.green, custom_id='tickets:1')
    async def tickets(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        creatingmessage = await interaction.response.send_message('The ticket is being created...', ephemeral=True)
        
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM ticketdatabase WHERE guild_id=?', (interaction.guild.id, ))
        rows = await cursor.fetchone()

        cursor2 = await db.execute('SELECT counter FROM ticketdatabase WHERE guild_id=?', (interaction.guild.id, ))
        counter = await cursor2.fetchone()
        await db.execute('UPDATE ticketdatabase SET counter=counter + ? WHERE guild_id=?', (1, interaction.guild.id))
        await db.commit()

        category_channel = interaction.guild.get_channel(rows[1])
        ticket_channel = await category_channel.create_text_channel(
            f"ticket-{counter[0]}")
        await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                                         send_messages=False,
                                         read_messages=False)


        role_ids = eval(rows[2])

        for role_id in role_ids:
            role = interaction.guild.get_role(role_id)
            
            await ticket_channel.set_permissions(role,
                                             send_messages=True,
                                             read_messages=True,
                                             add_reactions=True,
                                             embed_links=True,
                                             read_message_history=True,
                                             external_emojis=True)
        
        await ticket_channel.set_permissions(interaction.user,
                                         send_messages=True,
                                         read_messages=True,
                                         add_reactions=True,
                                         embed_links=True,
                                         attach_files=True,
                                         read_message_history=True,
                                         external_emojis=True)

        await interaction.edit_original_message(content=f'The ticket has been created at {ticket_channel.mention}.')

        x = f'{interaction.user.mention}'

        view = TicketClose()

      
        embed=discord.Embed(title="", 
        description=f"Support will be with you shortly!", 
        color=discord.Color.green())

        embed.set_footer(text="Close this ticket by clicking the 🔒 button.")

        em = discord.Embed(title="Responses",
                            description=f"Maybe?",
                            color=discord.Color.green())

        view = TicketClose()

        await ticket_channel.send(embeds=[embed, em], content=x, view=view)

class TicketClose(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji='🔒', style=discord.ButtonStyle.gray, custom_id='ticketclose')
    async def ticketclose(self, interaction: discord.Interaction, button: discord.ui.Button):

        msg = [interaction.message async for interaction.message in interaction.channel.history(oldest_first=True, limit=1)]

        x = msg[0].mentions[0].id
        y = msg[0].mentions[0]

        if x == interaction.user.id:

            await interaction.response.send_message('Closing the ticket...', ephemeral=True)

            await interaction.channel.set_permissions(interaction.user,
                                         send_messages=False,
                                         read_messages=False,
                                         add_reactions=False,
                                         embed_links=False,
                                         attach_files=False,
                                         read_message_history=False,
                                         external_emojis=False)

            closed = discord.utils.get(interaction.guild.channels, name="Closed Tickets")
            await interaction.channel.edit(category=closed)

            #view = AdminTicket()
            embed = discord.Embed(
                title="",
                description=
                f"Ticket Closed by {interaction.user.mention}",
                color=discord.Color.red())
            #await interaction.channel.send(embed=embed, view=view)
            await interaction.channel.send(embed=embed)
            await interaction.edit_original_message(content='Successfully closed the ticket!')
            for item in self.children:
                item.disabled = True
            await interaction.message.edit(view=self)
            return

        else:

            await interaction.response.send_message('Closing the ticket...', ephemeral=True)

            await interaction.channel.set_permissions(y,
                                         send_messages=False,
                                         read_messages=False,
                                         add_reactions=False,
                                         embed_links=False,
                                         attach_files=False,
                                         read_message_history=False,
                                         external_emojis=False)

            closed = discord.utils.get(interaction.guild.channels, name="Closed Tickets")
            await interaction.channel.edit(category=closed)

            #view = AdminTicket()
            embed = discord.Embed(
                title="",
                description=
                f"Ticket Closed by {interaction.user.mention}",
                color=discord.Color.red())
            #await interaction.channel.send(embed=embed, view=view)
            await interaction.channel.send(embed=embed)
            await interaction.edit_original_message(content='Successfully closed the ticket!')
            for item in self.children:
                item.disabled = True
            await interaction.message.edit(view=self)
            return

class TicketsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(TicketSystem())
        self.bot.add_view(TicketClose())

    @commands.command(name='tickets', hidden=True)
    @commands.is_owner()
    async def tickets(self, ctx):
        view = TicketSystem()
        await ctx.send('Click da button', view=view)

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))
