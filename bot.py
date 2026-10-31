import discord
from discord.ext import tasks, commands
from tfldata import get_disruptions
from dotenv import load_dotenv
import datetime
from zoneinfo import ZoneInfo
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

tz = ZoneInfo('Europe/London')
SIX_AM = datetime.time(hour=22, minute=57, tzinfo=tz)

def construct_message(MAX_LENGTH, data):
    messages = []
    message_lines = f"# TfL Disruptions\n"
    if data == []:
        message_lines += "No disruptions (according to TfL)!"
        messages.append(message_lines)
    else:
        for item in data:
            if len(message_lines) + len(item+"\n\n") > MAX_LENGTH:
                messages.append(message_lines)
                message_lines = item+"\n\n"
            else:
                message_lines += item+"\n\n"
        if message_lines:
            messages.append(message_lines)
    return messages

@tasks.loop(time=SIX_AM)
async def todo():
    MAX_LENGTH = 1900
    channel = bot.get_channel(CHANNEL_ID)
    disruptions = get_disruptions("64,466,433,314,157,154,280,45,tram,central,elizabeth")
    messages = construct_message(MAX_LENGTH, disruptions)
    for msg in messages:
        await channel.send(msg)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    if not todo.is_running():
        todo.start()
        print("disruptions report should now be in discord :)")

bot.run(str(BOT_TOKEN))