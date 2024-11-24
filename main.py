import os
from trello import TrelloClient
from dotenv import load_dotenv, dotenv_values 
import re
load_dotenv() 

print()

# Initialize the Trello client
client = TrelloClient(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("SECRET"),
    token=os.getenv("TOKEN"),  # Optional for public boards
)

# Get a public board by its ID or URL
board = client.get_board('/XyvHrkbi')

# Access lists and cards
for lst in board.list_lists():
    print(f'List: {lst.name}')
    for card in lst.list_cards():
        print(f'  Card: {card.name}')
        print(f'    labels: {[label.name for label in card.labels]}')
        # print(f'    info: {card.description}')
        # print(f'    attachments: {card.attachments}')
        for attachment in card.attachments:
            "".startswith("https://trello.com/c/")
            if attachment["url"].startswith("https://trello.com/c/"):
                match = re.search(r'/c/([^/]+)', attachment["url"]);
                card_id = ""
                if match and attachment['url'] != card.shortUrl:
                    card_id = match.group(1)
                    new_card = client.get_card(card_id)
                    print("    attached card:")
                    print(f'      Card: {new_card.name}')
                    print(f'        labels: {[label.name for label in card.labels]}')
                else:
                    print(f"    failed attached card: {attachment['name']}")
