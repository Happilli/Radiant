import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from webserver import keep_alive

# Load environment variables
# load_dotenv()
TOKEN = os.environ['CYPHER']

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.typing = False
intents.presences = False

# Define custom prefix
custom_prefix = commands.when_mentioned_or('R!', 'r!')

# Create the bot with custom prefix and intents
bot = commands.Bot(command_prefix=custom_prefix, intents=intents, help_command=None)

@bot.event
async def on_member_join(member):
    channel_id = 1145957203979808850
    channel = bot.get_channel(channel_id)
    
    # Load the GIF as the background
    gif_url = "https://cdn.discordapp.com/attachments/1145967795184607282/1145983601817690142/4PHg.gif"
    
    # Create an embedded message for join
    join_embed = discord.Embed(color=discord.Color.blue())
    join_embed.set_image(url=gif_url)
    join_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)  # Display the user's avatar as thumbnail
    join_embed.add_field(name=f"Welcome to the server, {member.name}!", value=f"We're glad to have you here.\n{member.mention}\n Have fun and alot of fun !")
    
    await channel.send(embed=join_embed)

@bot.event
async def on_member_remove(member):
    channel_id = 1145961145254023238 # Replace with the specific channel ID
    channel = bot.get_channel(channel_id)
    
    # Load the GIF as the background
    gif_url = "https://cdn.discordapp.com/attachments/1145967795184607282/1145983629667876874/Lpow.gif"
    
    # Create an embedded message for leave
    leave_embed = discord.Embed(color=discord.Color.red())
    leave_embed.set_image(url=gif_url)
    leave_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)  # Display the user's avatar as thumbnail
    leave_embed.add_field(name=f"{member.name} has left the server.", value=f"Goodbye, {member.name}!")

    await channel.send(embed=leave_embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

keep_alive()
bot.run(TOKEN)
