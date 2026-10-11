import discord
from tfldata import get_disruptions
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def construct_message(MAX_LENGTH, mode, data):
    messages = []
    message_lines = f"# TfL Disruptions: {mode.upper()} \n"
    if data == []:
        message_lines += "No disruptions (according to TfL)!"
        messages.append(message_lines)
    else:
        for item in data:
            routes = f"\nAffected routes: {item["affectedRoutes"]}" if item["affectedRoutes"] else ""
            stops = f"\nAffected Stops: {item["affectedStops"]}" if item["affectedStops"] else ""
            line_str = f"**{item["description"]}** {routes} {stops} \n\n"

            if len(message_lines) + len(line_str) > MAX_LENGTH:
                messages.append(message_lines)
                message_lines = line_str
            else:
                message_lines += line_str
        if message_lines:
            messages.append(message_lines)
    return messages

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    tube = get_disruptions("tube")
    train = get_disruptions("national-rail")
    tram = get_disruptions("tram")
    bus = get_disruptions("bus")
    
    MAX_LENGTH = 1900

    tube_messages = construct_message(MAX_LENGTH, "tube", tube)
    for msg in tube_messages:
        await channel.send(msg)

    train_messages = construct_message(MAX_LENGTH, "train", train)
    for msg in train_messages:
        await channel.send(msg)

    tram_messages = construct_message(MAX_LENGTH, "tram", tram)
    for msg in tram_messages:
        await channel.send(msg)

    bus_messages = construct_message(MAX_LENGTH, "bus", bus)
    for msg in bus_messages:
        await channel.send(msg)

client.run(BOT_TOKEN)