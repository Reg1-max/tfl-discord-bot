import requests

def get_disruptions(mode):
    r = requests.get(f'https://api.tfl.gov.uk/Line/Mode/{mode}/Disruption').json()
    i = 0
    while i < len(r):
        item = r[i]
        if item["category"] != "RealTime" or (item["category"] == "Information" and "nationalrail" not in item["description"]):
            r.pop(i)
        else:
            item = {"description":item["description"], "affectedRoutes":item["affectedRoutes"], "affectedStops":item["affectedStops"]}
            r[i] = item
        i += 1
    return r