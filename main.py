import discord
from discord.ext import commands
from discord.ui import Button, View
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")

# Flask pour Render
app = Flask('')

@app.route('/')
def home():
    return "Bot online"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
CATEGORY_ID = 1505338661078696046
LOGS_CHANNEL_ID = 1505338942633807995

# Bot prêt
@bot.event
async def on_ready():

    activity = discord.Game(name="pix3l.fr")

    await bot.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print(f"Connecté en tant que {bot.user}")

# Panel ticket
@bot.command()
async def panel(ctx):

    embed = discord.Embed(
        title="🎫 Support",
        description="Clique sur le bouton ci-dessous pour ouvrir un ticket.",
        color=discord.Color.blurple()
    )

    button = Button(
        label="Ouvrir un Ticket",
        style=discord.ButtonStyle.green,
        emoji="🎫"
    )

    async def button_callback(interaction):

        guild = interaction.guild

        category = discord.utils.get(
            guild.categories,
            id=CATEGORY_ID
        )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        # Bouton fermer
        close_button = Button(
            label="Fermer le Ticket",
            style=discord.ButtonStyle.red,
            emoji="🔒"
        )

        async def close_callback(close_interaction):

            await close_interaction.channel.delete()

        close_button.callback = close_callback

        close_view = View()
        close_view.add_item(close_button)

        # Embed ticket
        ticket_embed = discord.Embed(
            title="🎫 Ticket Créé",
            description="Le support va bientôt vous répondre.",
            color=discord.Color.green()
        )

        ticket_embed.add_field(
            name="Utilisateur",
            value=interaction.user.mention,
            inline=False
        )

        await channel.send(
            interaction.user.mention,
            embed=ticket_embed,
            view=close_view
        )

        # Logs
        logs_channel = bot.get_channel(
            LOGS_CHANNEL_ID
        )

        if logs_channel:

            log_embed = discord.Embed(
                title="📁 Ticket Créé",
                color=discord.Color.blurple()
            )

            log_embed.add_field(
                name="Utilisateur",
                value=interaction.user.mention,
                inline=False
            )

            log_embed.add_field(
                name="Salon",
                value=channel.mention,
                inline=False
            )

            await logs_channel.send(
                embed=log_embed
            )

        await interaction.response.send_message(
            f"✅ Ticket créé : {channel.mention}",
            ephemeral=True
        )

    button.callback = button_callback

    view = View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

# Lance Flask
keep_alive()

# Lance Discord
bot.run(TOKEN)