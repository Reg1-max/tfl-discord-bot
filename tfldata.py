import requests

def get_disruptions(mode):
    r = requests.get(f'https://api.tfl.gov.uk/Line/Mode/{mode}/Disruption').json()
    r = list(filter(lambda item: not(item["category"] == "Information" and "nationalrail" not in item["description"]), r))
    return r