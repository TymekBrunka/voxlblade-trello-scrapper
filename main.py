import os
from trello import TrelloClient
from dotenv import load_dotenv, dotenv_values 
import re
import json
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

# Access lists and cards
for lst in board.list_lists():
    print(f'List: {lst.name}')
    data[lst.name] = {}
    for card in lst.list_cards():
        print(f'  Card: {card.name}')
        data[lst.name][card.name] = {}
        # labels = [label.name for label in card.labels]
        # data[lst.name][card.name]["labels"] = labels
        data[lst.name][card.name]["labels"] = [label.name for label in card.labels]
        # print(f'    labels: {labels}')
        data[lst.name][card.name]["description"] = card.description;
        # print(f'    info: {card.description}')
        for attachment in card.attachments:
            if attachment["url"].startswith("https://trello.com/c/"):
                match = re.search(r'/c/([^/]+)', attachment["url"]);
                card_id = ""
                if match and attachment['url'] != card.shortUrl:
                    data[lst.name][card.name]["attachments"] = []
                    card_id = match.group(1)
                    new_card = client.get_card(card_id)
                    print("    attached card:")
                    # print(f"    on list: {new_card.get_list().name}")
                    print(f'      Card: {new_card.name}')
                    data[lst.name][card.name]["attachments"].append(f"{new_card.get_list().name}.{new_card.name}")
                    # print(f'        labels: {[label.name for label in card.labels]}')
                else:
                    # print(f"    failed attached card: {attachment['name']}")
                    pass

print("\n\n\n\n")
with open("./voxl-dumped.json", "w") as f:
    f.write(json.dumps(data, indent=2));
