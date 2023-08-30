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


bot = commands.Bot(command_prefix=['R!','r!','r','R'], intents=intents,  help_command=None)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="Here's a list of available commands:",
        color=discord.Color.green()
    )

    # Add commands and their descriptions
    commands_info = [
        ("**Avatar (`avt`)**", "Displays the avatar of a user."),
        ("**Ping (`ping`)**", "Displays the bot's latency."),
        ("**Welcome (`radiant`)**", "Displays a welcome message."),
        ("**Updates (`updates`)**", "Displays the current roadmap updates."),
        ("**Clear (`clear`)**", "Clears a specified number of messages from the channel."),
      ("**Calculator (`calc`)**","Does simple arthemetics."),
      ("**Tag (`tag`)**","Run the command to see available sub-commands.")
    ]

    for command_info in commands_info:
        embed.add_field(name=command_info[0], value=command_info[1], inline=False)

    embed.set_footer(text="Use the provided commands to interact with the bot!")

    await ctx.send(embed=embed)


# Load existing tags from a JSON file
TAGS_FILE = "tags/tags.json"

def load_tags():
    try:
        with open(TAGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save tags to a JSON file
def save_tags():
    with open(TAGS_FILE, "w") as file:
        json.dump(tags, file, indent=4)

# Load tags when the bot starts
tags = load_tags()



@bot.command()
async def tag(ctx, action: str, *args):
    if action == "create":
        tag_name = args[0]
        tag_content = " ".join(args[1:])
        if tag_name not in tags:
            tags[tag_name] = {
                'content': tag_content,
                'creator': ctx.author.id
            }
            save_tags()  # Save tags after updating
            embed = discord.Embed(
                title="Tag Created",
                description=f"Tag '{tag_name}' created successfully!",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Tag Already Exists",
                description=f"Tag '{tag_name}' already exists. Use `!tag edit` to modify it.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)


    elif action == "transfer":
        tag_name = args[0]
        target_user = ctx.message.mentions[0]
        if tag_name in tags:
            if tags[tag_name]['creator'] == ctx.author.id:
                tags[tag_name]['creator'] = target_user.id
                save_tags()  # Save tags after updating
                embed = discord.Embed(
                    title="Tag Transferred",
                    description=f"Tag '{tag_name}' transferred to {target_user.mention} successfully!",
                    color=0x00FF00
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Permission Denied",
                    description="You don't have permission to transfer this tag.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Tag Not Found",
                description=f"Tag '{tag_name}' doesn't exist.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
    

      
    elif action == "delete":
        tag_name = args[0]
        if tag_name in tags:
            if tags[tag_name]['creator'] == ctx.author.id:
                del tags[tag_name]
                save_tags()  # Save tags after updating
                embed = discord.Embed(
                    title="Tag Deleted",
                    description=f"Tag '{tag_name}' deleted successfully!",
                    color=0x00FF00
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Permission Denied",
                    description="You don't have permission to delete this tag.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Tag Not Found",
                description=f"Tag '{tag_name}' doesn't exist.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    elif action == "edit":
        tag_name = args[0]
        if tag_name in tags:
            if tags[tag_name]['creator'] == ctx.author.id:
                new_content = " ".join(args[1:])
                tags[tag_name]['content'] = new_content
                save_tags()  # Save tags after updating
                embed = discord.Embed(
                    title="Tag Edited",
                    description=f"Tag '{tag_name}' edited successfully!",
                    color=0x00FF00
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Permission Denied",
                    description="You don't have permission to edit this tag.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Tag Not Found",
                description=f"Tag '{tag_name}' doesn't exist.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    elif action == "list":
        user = ctx.message.mentions[0] if len(args) > 0 else ctx.author
        user_tags = [tag_name for tag_name, tag_data in tags.items() if tag_data['creator'] == user.id]
        if user_tags:
            tag_list = "\n".join(user_tags)
            embed = discord.Embed(
                title=f"{user.name}'s Tags",
                description=tag_list,
                color=0x7289DA
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="No Tags",
                description=f"{user.mention} has no tags.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    else:  # View a tag's content
        tag_name = action
        if tag_name in tags:
            embed = discord.Embed(
                title=f"Tag: {tag_name}",
                description=tags[tag_name]['content'],
                color=0x7289DA
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Tag Not Found",
                description=f"Tag '{tag_name}' doesn't exist.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    

@bot.command(name='tagcmds', brief='Show available commands and descriptions')
async def show_help(ctx):
    embed = discord.Embed(
        title='Tag Bot Help',
        description='Here are the available commands:',
        color=0x7289DA
    )
    
    # Add descriptions for each command
    commands_info = [
        ('create', 'Create a new tag. Usage: `!tag create <tag_name> <tag_content>`'),
        ('delete', 'Delete a tag you created. Usage: `!tag delete <tag_name>`'),
        ('edit', 'Edit the content of a tag you created. Usage: `!tag edit <tag_name> <new_content>`'),
        ('list', 'List all tags created by a user. Usage: `!tag list [@user]`'),
        ('view', 'View the content of a specific tag. Usage: `!tag <tag_name>`'),
        ('transfer', 'Transfer ownership of a tag you created. Usage: `!tag transfer <tag_name> <@target_user>`')
    ]
    
    for command, description in commands_info:
        embed.add_field(name=f'!tag {command}', value=description, inline=False)
    
    await ctx.send(embed=embed)









@bot.command()
async def calc(ctx, *, expression: str):
    try:
        result = eval(expression)
        embed = discord.Embed(
            title="Calculator",
            description=f"Expression: {expression}\nResult: {result}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="Calculator",
            description=f"An error occurred: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)



@bot.command()
async def avt(ctx, user: discord.User = None):
    user = user or ctx.author
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    embed = discord.Embed(title=f"{user.name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=avatar_url)
    embed.add_field(name="Avatar URL", value=f"[Click Here]({avatar_url})")  # Make the URL clickable
    
    await ctx.send(embed=embed)



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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Command Not Found",
            description="The command you entered does not exist.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# Event: Message received
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself

    await bot.process_commands(message)  # Process commands in the message



PROFILES_FILE = "profiles/profiles.json"

# Load profiles from the JSON file
def load_profiles():
    try:
        with open(PROFILES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save profiles to the JSON file
def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

# Load profiles when the bot starts
profiles = load_profiles()

@bot.command()
async def profile(ctx, user: discord.Member = None):
    user = user or ctx.author
    user_id = str(user.id)
    
    if user_id in profiles:
        profile_data = profiles[user_id]
        name = profile_data.get("name", "N/A")
        age = profile_data.get("age", "N/A")
        affiliation = profile_data.get("affiliation", "N/A")
        social_media = profile_data.get("social_media", "N/A")
        
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        
        embed = discord.Embed(title=f"{user.name}'s Profile", color=0x7289DA)
        embed.set_thumbnail(url=avatar_url)  # Set the grabbed avatar as the thumbnail
        
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Age", value=age, inline=False)
        embed.add_field(name="Affiliation", value=affiliation, inline=False)
        embed.add_field(name="Social Media", value=f"[View]({social_media})", inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{user.display_name} doesn't have a profile. Use `r!profile_config` to create one.")


@bot.command()
async def profile_delete(ctx):
    user_id = str(ctx.author.id)
    if user_id in profiles:
        del profiles[user_id]
        save_profiles(profiles)
        await ctx.send("Your profile has been deleted.")
    else:
        await ctx.send("You don't have a profile to delete.")

@bot.command()
async def profile_config(ctx, field: str, *, value: str):
    allowed_fields = ["name", "age", "affiliation", "social_media"]
    if field.lower() in allowed_fields:
        user_id = str(ctx.author.id)
        if user_id not in profiles:
            profiles[user_id] = {}
        profiles[user_id][field.lower()] = value
        save_profiles(profiles)
        await ctx.send(f"Your {field} has been updated.")
    else:
        await ctx.send(f"Invalid field. Allowed fields: {', '.join(allowed_fields)}")

@bot.command()
async def config_help(ctx):
    allowed_fields = {
        "name": "Your Name",
        "age": "Your Age",
        "affiliation": "Your Affiliation",
        "social_media": "Your Social Media Link"
    }
    
    embed = discord.Embed(title="Possible Configuration Fields", color=0x7289DA)
    field_list = "\n".join([f"`{field}`: {example}" for field, example in allowed_fields.items()])
    embed.add_field(name="Fields and Examples", value=field_list, inline=False)
    embed.set_footer(text="Use r!profile_config [field] [value] to configure your profile.")
    
    await ctx.send(embed=embed)

keep_alive() 
bot.run(TOKEN)
