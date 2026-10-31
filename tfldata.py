import requests

def get_disruptions(ids):
    r = requests.get(f'https://api.tfl.gov.uk/Line/{ids}/Status?detail=true').json()
    ls = []
    for i in r:
      lineStatuses = i["lineStatuses"]
      for j in lineStatuses:
         if j["statusSeverity"] != 10:
            ls.append(j["reason"])

    seen = []
    i = 0
    while i < len(ls):
        if ls[i] not in seen:
            seen.append(ls[i])
        i += 1

    return seen