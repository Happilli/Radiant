import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
from webserver import keep_alive
import asyncio
import math
import random 
from PIL import Image
import requests


#load_dotenv()
TOKEN = os.environ['CYPHER']
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.typing = False
intents.presences = False


bot = commands.Bot(command_prefix=['R!','r!','r','R'], intents=intents)


@bot.command()
async def avt(ctx, user: discord.User = None):
    user = user or ctx.author
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    embed = discord.Embed(title=f"{user.name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=avatar_url)
    
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel_id = 1145957203979808850  # Replace with the specific channel ID
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


@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # Convert to milliseconds

    ping_embed = discord.Embed(color=discord.Color.green())
    ping_embed.add_field(name='Ping', value=f'Latency: {latency:.2f}ms')

    await ctx.send(embed=ping_embed)

@bot.command()
async def radiant(ctx):
    embed = discord.Embed(color=discord.Color.blue())

    # Set the background image
    background_image_url = "https://cdn.discordapp.com/attachments/1145967795184607282/1146006090224500756/cc3a3648a5c246a0012190327a081108.jpg"
    embed.set_image(url=background_image_url)

    # Set the icon image for "Radiant Bot"
    icon_url = "https://cdn.discordapp.com/attachments/1145967795184607282/1146005557451436032/98142dc4d64357ddd72c736ef58b9b0f.jpg"
    embed.set_author(name="Radiant Bot", icon_url=icon_url)

    # Add a stylish title and description
    embed.title = "Welcome to Radiant Bot!!"
    embed.description = (
        "Radiant Bot is an exclusive Happillis's server bot that manages this server only! "
        "Use various commands to interact and have fun!"
    )

    # Add links with a more elegant format
    embed.add_field(
        name="Links",
        value="[GitHub](https://github.com/happilli) • [Facebook](https://facebook.com/safal.lama.726)",
        inline=False
    )

    # Set a stylish footer
    embed.set_footer(text="Enjoy your time with Radiant Bot!", icon_url=icon_url)

    await ctx.send(embed=embed)

@bot.command()
async def roadmap(ctx):
    allowed_user_id = 1128651413535346708  # Replace with the allowed user's ID

    if ctx.author.id != allowed_user_id:
        await ctx.send("You are not authorized to use this command.")
        return

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    embed = discord.Embed(title="Roadmap Updates", description="Please provide the planned updates for the roadmap. Type each update on a new line.\nType `done` when you're finished.", color=discord.Color.blue())
    await ctx.send(embed=embed)

    updates = []
    while True:
        try:
            user_input = await bot.wait_for("message", check=check, timeout=300)
            if user_input.content.lower() == "done":
                break
            updates.append(user_input.content)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to provide updates. Command cancelled.")
            return

    if updates:
        updates_text = "\n".join(updates)

        confirmation_embed = discord.Embed(title="Confirm Updates", description=f"The following updates will be added to the roadmap:\n\n{updates_text}\n\nDo you want to save these updates?", color=discord.Color.blue())
        confirm_msg = await ctx.send(embed=confirmation_embed)

        try:
            await confirm_msg.add_reaction("✅")
            await confirm_msg.add_reaction("❌")

            reaction, _ = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in ["✅", "❌"], timeout=60)

            if reaction.emoji == "✅":
                with open("assets/updates.txt", "a") as file:  # Use "a" for append mode
                    file.write(updates_text + "\n")
                await ctx.send("Changes have been recorded.")
            else:
                await ctx.send("Changes were not saved.")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to confirm. Changes were not saved.")
    else:
        await ctx.send("No updates provided. Command cancelled.")  



@bot.command()
async def updates(ctx):
    embed = discord.Embed(title="Roadmap Updates", color=discord.Color.green())

    try:
        with open("assets/updates.txt", "r") as file:
            updates = file.read().strip().split('\n')

        if updates:
            formatted_updates = ""
            for idx, update in enumerate(updates, start=1):
                formatted_updates += f"{idx}. {update}\n"

            formatted_updates = f"```\n{formatted_updates}\n```"
            embed.add_field(name="Updates", value=formatted_updates, inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1145967795184607282/1146005557451436032/98142dc4d64357ddd72c736ef58b9b0f.jpg")
            embed.set_footer(text="These projects are incomplete and will be in work soon.")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No updates available.")
    except FileNotFoundError:
        await ctx.send("No updates available.")





# Load restricted user IDs from the text file
def load_restricted_users():
    try:
        with open('assets/restricted_users.txt', 'r') as file:
            return set(int(line.strip()) for line in file)
    except FileNotFoundError:
        return set()

# Save restricted user IDs to the text file
def save_restricted_users(restricted_users):
    with open('assets/restricted_users.txt', 'w') as file:
        for user_id in restricted_users:
            file.write(str(user_id) + '\n')

# Initialize restricted user IDs from the text file
restricted_users = load_restricted_users()

# Restrict command to add a user to the restricted list
@bot.command()
async def restrict(ctx, user: discord.User):
    if ctx.author.id == 1128651413535346708:  # Replace with your own user ID
        restricted_users.add(user.id)
        save_restricted_users(restricted_users)
        await ctx.send(f"{user.mention} has been restricted from using the bot.")
    else:
        await ctx.send("You do not have permission to use this command.")

# Unrestrict command to remove a user from the restricted list
@bot.command()
async def unrestrict(ctx, user: discord.User):
    if ctx.author.id == 1128651413535346708:  # Replace with your own user ID
        if user.id in restricted_users:
            restricted_users.remove(user.id)
            save_restricted_users(restricted_users)
            await ctx.send(f"{user.mention} has been unrestricted and can now use the bot.")
        else:
            await ctx.send(f"{user.mention} is not currently restricted.")
    else:
        await ctx.send("You do not have permission to use this command.")

# Check if a user is restricted before processing commands
@bot.check
async def is_user_restricted(ctx):
    if ctx.author.id in restricted_users:
        embed = discord.Embed(
            title="Restricted User",
            description="Sorry, you are currently restricted from using bot commands.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return False  # Returning False will prevent the command from being executed
    return True




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Clear command to delete messages from a channel
@bot.command()
async def clear(ctx, amount: int):
    if ctx.author.id == 1128651413535346708:  # Replace with your own user ID
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Cleared {amount} messages.", delete_after=5)  # Send a confirmation message
    else:
        await ctx.send("You do not have permission to use this command.")
  

keep_alive() 
bot.run(TOKEN)
