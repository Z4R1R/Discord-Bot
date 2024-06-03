import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize variables
codes_list = []
used_codes = []
users_waiting_for_code = []
timer_running = False
code_word_channel_id = None
codes_file = "codes.txt"
channel_file = "channel.txt"

# Function to load codes from a file
def load_codes():
    if os.path.exists(codes_file):
        with open(codes_file, "r") as file:
            return file.read().splitlines()
    return []

# Function to save used codes back to the file
def save_codes(codes):
    with open(codes_file, "w") as file:
        file.write("\n".join(codes))

# Function to load the code-word channel ID from a file
def load_channel():
    if os.path.exists(channel_file):
        with open(channel_file, "r") as file:
            return int(file.read().strip())
    return None

# Function to save the code-word channel ID to a file
def save_channel(channel_id):
    with open(channel_file, "w") as file:
        file.write(str(channel_id))

@bot.event
async def on_ready():
    global codes_list
    global code_word_channel_id
    codes_list = load_codes()
    code_word_channel_id = load_channel()
    print(f'Logged in as {bot.user}')

@bot.command(name="start_timer")
@commands.has_permissions(administrator=True)
async def start_timer(ctx):
    global timer_running
    timer_running = True
    await ctx.send("Timer started. Users can now send the specific word to receive codes.")

@bot.command(name="stop_timer")
@commands.has_permissions(administrator=True)
async def stop_timer(ctx):
    global timer_running
    timer_running = False
    await ctx.send("Timer stopped. Distributing codes to users who have used the specific word...")

    for user in users_waiting_for_code:
        if not codes_list:
            await user.send("Sorry, no codes left.")
            break
        code = codes_list.pop(0)
        used_codes.append(code)
        await user.send(f"Here's your code: {code}")

    users_waiting_for_code.clear()
    save_codes(codes_list)

@bot.command(name="set_code_channel")
@commands.has_permissions(administrator=True)
async def set_code_channel(ctx, channel: discord.TextChannel):
    global code_word_channel_id
    code_word_channel_id = channel.id
    save_channel(code_word_channel_id)
    await ctx.send(f"Code-word channel set to {channel.mention}")

@bot.command(name="reload_codes")
@commands.has_permissions(administrator=True)
async def reload_codes(ctx):
    global codes_list
    codes_list = load_codes()
    await ctx.send("Codes reloaded from file.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    global timer_running
    global code_word_channel_id

    codeword = "deeznuts"
    
    if timer_running and message.channel.id == code_word_channel_id and codeword in message.content.lower():
        users_waiting_for_code.append(message.author)
        await message.author.send("You will receive a code shortly after the timer is stopped.")

    await bot.process_commands(message)

bot.run('MTI0NTc5OTA3OTMzMDQ1MTYyOA.GD5p9F.d4WRofQy-JtDoClyXibL4kgdYyQNYH2L88VxZc')