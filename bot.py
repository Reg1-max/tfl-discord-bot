# This example requires the 'message_content' intent.

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

def tube_message(MAX_LENGTH, tube_data):
    messages = []
    message_lines = "# TfL Disruptions: TUBE \n"
    if tube_data == []:
        message_lines += "No disruptions (according to TfL)!"
        messages.append(message_lines)
    else:
        for item in tube_data:
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

def train_message(MAX_LENGTH, train_data):
    messages = []
    message_lines = "# TfL Disruptions: TRAIN \n"
    if train_data == []:
        message_lines += "No disruptions (according to TfL)!"
        messages.append(message_lines)
    else:
        for item in train_data:
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

def tram_message(MAX_LENGTH, tram_data):
    messages = []
    message_lines = "# TfL Disruptions: TRAM \n"
    if tram_data == []:
        message_lines += "No disruptions (according to TfL)!"
        messages.append(message_lines)
    else:
        for item in tram_data:
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

def bus_message(MAX_LENGTH, bus_data):
    messages = []
    message_lines = "# TfL Disruptions: BUS \n"
    if bus_data == []:
        message_lines += "No disruptions (according to TfL)!"
        messages.append(message_lines)
    else:
        for item in bus_data:
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
    bus, tram, train, tube = get_disruptions()
    
    MAX_LENGTH = 1900

    tube_messages = tube_message(MAX_LENGTH, tube)
    for msg in tube_messages:
        await channel.send(msg)

    train_messages = train_message(MAX_LENGTH, train)
    for msg in train_messages:
        await channel.send(msg)

    tram_messages = tram_message(MAX_LENGTH, tram)
    for msg in tram_messages:
        await channel.send(msg)

    bus_messages = bus_message(MAX_LENGTH, bus)
    for msg in bus_messages:
        await channel.send(msg)

client.run(BOT_TOKEN)