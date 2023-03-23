import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    # type Local or Server
    parser.add_argument('--type', type=str, required=True)
    # Notion token
    parser.add_argument('--token', type=str, required=True)
    # database id 
    # https://www.notion.so/~~~/asdfasdfkljashdfklasdhf?v=...
    # -------------------------|<----database id----->|
    parser.add_argument('--database_id', type=str, required=True)

    args = parser.parse_args()
    json_dict = {
        'type': args.type,
        'token': args.token,
        'database_id': args.database_id
    }
    
    with open("notion.json", 'w') as f:
        json.dump(json_dict, f)
    
if __name__ == '__main__':
    main()