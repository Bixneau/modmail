import discord
from discord.ext import commands
import os

# Token sécurisé Render
TOKEN = os.getenv("TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Bot prêt
@bot.event
async def on_ready():

    activity = discord.Game(name="pix3l.fr")

    await bot.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print(f"Connecté en tant que {bot.user}")

# Commande ticket
@bot.command()
async def ticket(ctx):

    # ID catégorie tickets
    category_id = 1505338661078696046

    # ID salon logs
    logs_channel_id = 1505338942633807995

    guild = ctx.guild

    # Récupère catégorie
    category = discord.utils.get(
        guild.categories,
        id=category_id
    )

    # Création salon
    channel = await guild.create_text_channel(
        name=f"ticket-{ctx.author.name}",
        category=category
    )

    # Ping utilisateur
    await channel.send(
        f"{ctx.author.mention}"
    )

    # Embed ticket
    embed = discord.Embed(
        title="🎫 Nouveau Ticket",
        description="Le support va bientôt vous répondre.",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="Utilisateur",
        value=ctx.author.mention,
        inline=False
    )

    await channel.send(embed=embed)

    # Logs
    logs_channel = bot.get_channel(
        logs_channel_id
    )

    if logs_channel:

        log_embed = discord.Embed(
            title="📁 Ticket Créé",
            color=discord.Color.green()
        )

        log_embed.add_field(
            name="Utilisateur",
            value=ctx.author.mention,
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

    # Confirmation
    await ctx.send(
        f"✅ Ticket créé : {channel.mention}"
    )

# Lancement bot
bot.run(TOKEN)