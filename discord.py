import discord
from discord.ext import commands
import os

# Token sécurisé depuis Render
TOKEN = os.getenv("TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Quand le bot démarre
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

# Commande ticket
@bot.command()
async def ticket(ctx):

    guild = ctx.guild

    # Création du salon ticket
    channel = await guild.create_text_channel(
        name=f"ticket-{ctx.author.name}"
    )

    # Ping utilisateur
    await channel.send(f"{ctx.author.mention}")

    # Embed
    embed = discord.Embed(
        title="🎫 Nouveau Ticket",
        description="Un nouveau ticket a été créé.",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="Utilisateur",
        value=ctx.author.mention,
        inline=False
    )

    embed.add_field(
        name="ID",
        value=str(ctx.author.id),
        inline=False
    )

    embed.set_footer(text="Support Bot")

    # Envoi embed
    await channel.send(embed=embed)

    # Confirmation
    await ctx.send(f"✅ Ticket créé : {channel.mention}")

# Lancement du bot
bot.run(TOKEN)