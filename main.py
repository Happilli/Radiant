import discord
from discord.ext import commands
from discord import File
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import os
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()
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

    # Load the welcome background image
    background_image = Image.open("1.jpg")

    # Create a drawing context on the background image
    draw = ImageDraw.Draw(background_image)

    # Get the user's avatar URL
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

    async with bot.http_session.get(avatar_url) as response:
        if response.status == 200:
            avatar_data = await response.read()
            avatar_image = Image.open(BytesIO(avatar_data))

            # Modify the position and size of the avatar
            avatar_position = (25, 25)  # Change these values as needed
            avatar_size = (450, 450)     # Change these values as needed

            # Resize the avatar using the "NEAREST" filter and add an alpha channel
            avatar_image_resized = avatar_image.resize(avatar_size, Image.NEAREST)
            avatar_image_resized.putalpha(255)  # Add a fully opaque alpha channel

            # Create a circular mask for the avatar
            mask = Image.new('L', avatar_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=255)

            # Apply the circular mask to the avatar
            avatar_image_resized.putalpha(mask)

            # Paste the circular avatar onto the background with the new position and size
            background_image.paste(avatar_image_resized, avatar_position, avatar_image_resized)

            # Add a transparent black overlay at the bottom of the image
            black_overlay = Image.new('RGBA', background_image.size, (0, 0, 0, 128))
            background_image.paste(black_overlay, (0, background_image.height - 100), black_overlay)

            # Adjust the position of the welcome message
            font_size = 52
            font = ImageFont.truetype("Poppins.ttf", size=font_size)
            text = f"Welcome to the server, {member.display_name}!"
            text_x = (background_image.width - len(text) * (font_size // 2)) // 2
            text_y = (background_image.height - 100 + 24)
            outline_color = (255, 255, 255, 255)  # Add a comma to make it a tuple
            fill_color = (0, 255, 255, 255)  # Add a comma to make it a tuple
            draw.text((text_x, text_y), text, outline_color, font=font)
            draw.text((text_x, text_y), text, fill_color, font=font)

            # Save the generated image as bytes in memory
            temp_image = BytesIO()
            background_image.save(temp_image, format="PNG")
            temp_image.seek(0)

            # Send the temporary image to the channel
            await channel.send(file=File(temp_image, filename="welcome.png"))

@bot.event
async def on_member_remove(member):
    channel_id = 1145961145254023238
    channel = bot.get_channel(channel_id)

    # Load the goodbye background image
    background_image = Image.open("2.jpg")

    # Create a drawing context on the background image
    draw = ImageDraw.Draw(background_image)

    # Get the user's avatar URL
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

    async with bot.http_session.get(avatar_url) as response:
        if response.status == 200:
            avatar_data = await response.read()
            avatar_image = Image.open(BytesIO(avatar_data))

            # Modify the position and size of the avatar
            avatar_position = (25, 25)  # Change these values as needed
            avatar_size = (450, 450)     # Change these values as needed

            # Resize the avatar using the "NEAREST" filter and add an alpha channel
            avatar_image_resized = avatar_image.resize(avatar_size, Image.NEAREST)
            avatar_image_resized.putalpha(255)  # Add a fully opaque alpha channel

            # Create a circular mask for the avatar
            mask = Image.new('L', avatar_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=255)

            # Apply the circular mask to the avatar
            avatar_image_resized.putalpha(mask)

            # Paste the circular avatar onto the background with the new position and size
            background_image.paste(avatar_image_resized, avatar_position, avatar_image_resized)

            # Add a transparent black overlay at the bottom of the image
            black_overlay = Image.new('RGBA', background_image.size, (0, 0, 0, 128))
            background_image.paste(black_overlay, (0, background_image.height - 100), black_overlay)

            # Adjust the position of the goodbye message
            font_size = 52
            font = ImageFont.truetype("Poppins.ttf", size=font_size)
            text = f"{member.display_name} has left the server."
            text_x = (background_image.width - len(text) * (font_size // 2)) // 2
            text_y = (background_image.height - 100 + 24)
            outline_color = (255, 255, 255, 255)  # Add a comma to make it a tuple
            fill_color = (0, 255, 255, 255)  # Add a comma to make it a tuple
            draw.text((text_x, text_y), text, outline_color, font=font)
            draw.text((text_x, text_y), text, fill_color, font=font)

            # Save the generated image as bytes in memory
            temp_image = BytesIO()
            background_image.save(temp_image, format="PNG")
            temp_image.seek(0)

            # Send the temporary image to the channel
            await channel.send(file=File(temp_image, filename="goodbye.png"))

@bot.event
async def on_ready():
    bot.http_session = aiohttp.ClientSession()
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def clear(ctx, amount: int):
    # Check if the command is invoked by the specific user
    if ctx.author.id == 1128651413535346708:
        # Delete the command message
        await ctx.message.delete()

        # Delete 'amount' of messages in the current channel
        await ctx.channel.purge(limit=amount + 1)  # +1 to also delete the command message
    else:
        await ctx.send("You don't have permission to use this command.")


bot.run(TOKEN)
