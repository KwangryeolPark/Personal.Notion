import os
import socket
from datetime import datetime
from notion_client import Client

NOTION_TOKEN = "secret_MqjmE6xA5ynMXGtAfyu9BA6s9DTZQRAhMnqxbUaRAJ6" # os.environ["NOTION_TOKEN"]
NOTION_DATABASE_SERVER_API_ID = "eec8cad7dc044af6a64035e8fe813ffe"  # os.environ["NOTION_DATABASE_SERVER_API_ID"]
HOST = socket.gethostname()
IP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP.connect(("8.8.8.8", 80))
IP = IP.getsockname()[0]

assert len(NOTION_DATABASE_SERVER_API_ID) == 32

notion = Client(
    auth=NOTION_TOKEN
)

database = notion.databases.query(
    **{
        'database_id': NOTION_DATABASE_SERVER_API_ID
    }
)

# More information: https://developers.notion.com/reference/property-value-object#date-property-values
notion.pages.create(
    **{
        'parent': {
            'database_id': NOTION_DATABASE_SERVER_API_ID
        },
        'properties': {
            '이름': {
                'title': [
                    {
                        'type': 'text',
                        'text': {
                            'content': HOST
                        }
                    }
                ]
            },
            '종류': {
                'select': {
                    'name': 'Local',
                    'color': 'default'
                }
            },
            'IP': {
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': IP
                        }
                    }
                ]
            },
            '날짜': {
                'date': {
                    'start': datetime.today().strftime("%Y-%m-%d")
                }
            }
        }
    }
)