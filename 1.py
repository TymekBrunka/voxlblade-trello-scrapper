import os
from trello import TrelloClient
from dotenv import load_dotenv, dotenv_values 
import re
import json

from concurrent.futures import ThreadPoolExecutor #multithreading to speed up caching
load_dotenv() 

# Initialize the Trello client
client = TrelloClient(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("SECRET"),
    token=os.getenv("TOKEN"),  # Optional for public boards
)

data = {}
# Get a public board by its ID or URL
board = client.get_board('/XyvHrkbi')

def threaded_for(func, lst: list):
    if len(lst) > 0:
        with ThreadPoolExecutor(max_workers=len(lst)) as executor:
            results = list(executor.map(func, lst))
            results2 = results.copy()
            for v in results:
                if (v[1] == None):
                    results2.remove(v)
            return results2
    else:
        return []

def removeNones(dic: dict):
    lst = list(dic.items()).copy()
    for k, v in lst:
        if v == None:
            print(k, " true")
            lst.remove((k,v))
    return dict(lst)

def iter_cards(card):
    print(f'  Card: {card.name}')
    if (
        "hex" in card.description.lower()
        # "hex" in card.description.lower()
    ):
        return (card.name, {"url": card.url, "desc": card.description})
    else:
        return (card.name, None)
    # data[lst.name][card.name]["attachments"] = []
    # data[lst.name][card.name]["attachments"] = [ i["url"] if i["url"][19] == 'c' and i["url"] != card.shortUrl else '' for i in card.attachments]
    # for attachment in card.attachments:
    #     if attachment["url"][19] == 'c' and attachment['url'] != card.shortUrl:
    #         # data[lst.name][card.name]["attachments"].append(attachment["url"])
    #         pass

for lst in board.list_lists():
    if lst.name in [
        # "Handles",
        # "Blades",
        # "Fist Gloves",
        # "Fist Essence",
        "Weapon Arts",
        "Armor Sets",
        "Stats",
        "Runes",
        "Rings",
    ]:
        print(f'List: {lst.name}')
        data[lst.name] = dict(threaded_for(iter_cards, lst.list_cards()))
    # data[lst.name] = removeNones(data[lst.name])

with open("./cache.json", "w") as f:
    f.write(json.dumps(data, indent=2));
