import time
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def pred_threshold():
    www2=requests.get('https://api.mozambiquehe.re/predator?auth={token}'.format(token=os.getenv('APEX_TOKEN')))
    while www2.status_code==405:
        print('Fixing error 405...')
        time.sleep(5)
        www2=requests.get('https://api.mozambiquehe.re/predator?auth={token}'.format(token=os.getenv('APEX_TOKEN')))
    if www2.status_code==200:
        parsed_json=(json.dumps(www2.json()))
        a=(json.loads(parsed_json)["RP"]["PC"])
        b=(json.loads(parsed_json)["AP"]["PC"])
        return a['val'],a['totalMastersAndPreds'],b['val'],b['totalMastersAndPreds']
    else:
        print('ERROR',www2.status_code)

def jprint(obj):        # create a formatted string of the Python JSON object
    
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_rankScore(platform,player):
    www2=requests.get('https://api.mozambiquehe.re/bridge?auth={token}&player={player}&platform={platform}'.format(platform=platform, player=player, token=os.getenv('APEX_TOKEN')))
    while www2.status_code==405:
        print('Fixing error 405...')
        time.sleep(5)
        www2=requests.get('https://api.mozambiquehe.re/bridge?auth={token}&player={player}&platform={platform}'.format(platform=platform, player=player, token=os.getenv('APEX_TOKEN')))
    if www2.status_code==200:
        parsed_json=(json.dumps(www2.json()))
        a=(json.loads(parsed_json)["global"]["rank"])
        return a['rankName'], a['rankScore']
    else:
        print('ERROR',www2.status_code)

def map_rotation_data():
    www2=requests.get('https://api.mozambiquehe.re/maprotation?auth={token}'.format(token=os.getenv('APEX_TOKEN')))
    while www2.status_code==405:
        print('Fixing error 405...')
        time.sleep(5)
        www2=requests.get('https://api.mozambiquehe.re/maprotation?auth={token}'.format(token=os.getenv('APEX_TOKEN')))
    if www2.status_code==200:
        parsed_json=(json.dumps(www2.json()))
        a=(json.loads(parsed_json)["current"])
        b=(json.loads(parsed_json)["next"])
        return a['map'],a['remainingTimer'],b['map'],b['readableDate_start'],b['readableDate_end']
    else:
        print('ERROR',www2.status_code)