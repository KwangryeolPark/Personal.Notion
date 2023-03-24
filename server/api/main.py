import os
import json
import socket
import time
import argparse
import sys
from datetime import datetime
from notion_client import Client

DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(DIR, './notion.json')
IP_PATH = os.path.join(DIR, './ip.txt')
parser = argparse.ArgumentParser()

def check_json():
    if os.path.exists(JSON_PATH) == False:
        raise FileExistsError(f"There is no file {JSON_PATH}\nPlease execute generate_info.py with --type --token --database_id.")
    
def get_json():
    json_val = None
    with open(JSON_PATH, 'r') as f:
        json_val = json.load(f)
    return json_val

def check_last_ip(IP):
    if os.path.exists(IP_PATH):
        with open(IP_PATH, 'r+') as f:
            last_ip = f.read()
            if last_ip == IP:
                return 0
            else:
                f.truncate(0)
                f.write(IP)
                return 1
    else:
        with open(IP_PATH, 'w') as f:
            f.write(IP)
            return 2
        
def main():
    print(f"PID: {os.getpid()}", flush=True)

    HOST = socket.gethostname()
    IP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP.connect(("8.8.8.8", 80))
    IP = IP.getsockname()[0]
    
    if check_last_ip(IP) != 0:
        print(f'IP is updated to {IP}', flush=True)
        try:
            check_json()
            json_val = get_json()
            
            NOTION_TOKEN = json_val['token']
            NOTION_DATABASE_SERVER_API_ID = json_val['database_id']
        

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
                                'name': json_val['type'],
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
        except:
            print(f'Current time: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}', file=sys.stderr, flush=True)
            if os.path.exists(IP_PATH):
                with open(IP_PATH, 'w') as f:
                    f.truncate(0)
        print(f'Current time: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}', flush=True)
        
if __name__ == "__main__":
    parser.add_argument('-l', '--loop', type=bool, default=False)
    args = parser.parse_args()
    
    main()
    if args.loop == True:
        while True:
            time.sleep(60 * 60) # One hour
            main()