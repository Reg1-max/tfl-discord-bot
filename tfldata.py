import requests
import json

r = requests.get('https://api.tfl.gov.uk/Line/Mode/tube,tram,national-rail,bus/Disruption')

# we need categories that are RealTime AND descriptions that contain "nationalrail"

buses = requests.get('https://api.tfl.gov.uk/Line/Mode/bus/Disruption')
trains = requests.get('https://api.tfl.gov.uk/Line/Mode/national-rail/Disruption')
tube = requests.get('https://api.tfl.gov.uk/Line/Mode/tube/Disruption')
tram = requests.get('https://api.tfl.gov.uk/Line/Mode/tram/Disruption')

bus_processed = buses.json()
trains_processed = trains.json()
tube_processed = tube.json()
tram_processed = tram.json()

i = 0
while i < len(bus_processed):
    item = bus_processed[i]
    if item["category"] != "RealTime":
        bus_processed.pop(i)
    i += 1

i = 0
while i < len(tram_processed):
    item = tram_processed[i]
    if item["category"] != "RealTime":
        tram_processed.pop(i)
    i += 1

i = 0
while i < len(tube_processed):
    item = tube_processed[i]
    if item["category"] != "RealTime":
        tube_processed.pop(i)
    i += 1

i = 0
while i < len(trains_processed):
    item = trains_processed[i]
    if item["category"] != "RealTime" and "nationalrail" not in item["description"]:
        trains_processed.pop(i)
    i += 1
