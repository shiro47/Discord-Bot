import time
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def jprint(obj):        # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

##########################################APEX LEGENDS#################################################

def pred_threshold():
    www2=requests.get('https://api.mozambiquehe.re/predator?auth={token}'.format(token=os.getenv('APEX_TOKEN')))
    while www2.status_code!=200:
        print(f'Fixing error {www2.status_code}...')
        time.sleep(5)
        www2=requests.get('https://api.mozambiquehe.re/predator?auth={token}'.format(token=os.getenv('APEX_TOKEN')))
    if www2.status_code==200:
        parsed_json=(json.dumps(www2.json()))
        a=(json.loads(parsed_json)["RP"]["PC"])
        b=(json.loads(parsed_json)["AP"]["PC"])
        return a['val'],a['totalMastersAndPreds'],b['val'],b['totalMastersAndPreds']
    else:
        print('ERROR',www2.status_code)

def get_rankScore(platform,player):
    www2=requests.get('https://api.mozambiquehe.re/bridge?auth={token}&player={player}&platform={platform}'.format(platform=platform, player=player, token=os.getenv('APEX_TOKEN')))
    while www2.status_code!=200:
        print(f'Fixing error {www2.status_code}...')
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
    while www2.status_code!=200:
        print(f'Fixing error {www2.status_code}...')
        time.sleep(5)
        www2=requests.get('https://api.mozambiquehe.re/maprotation?auth={token}'.format(token=os.getenv('APEX_TOKEN')))
    if www2.status_code==200:
        parsed_json=(json.dumps(www2.json()))
        a=(json.loads(parsed_json)["current"])
        b=(json.loads(parsed_json)["next"])
        return a['map'],a['remainingTimer'],b['map'],b['readableDate_start'],b['readableDate_end']
    else:
        print('ERROR',www2.status_code)

#################################################TWITCH###########################################################

def check_stream_status(streamer_name):
  client_id = os.getenv('TWITCH_CLIENT_ID')
  client_secret = os.getenv('TWITCH_CLIENT_SECRET')
  body = {
      'client_id': client_id,
      'client_secret': client_secret,
      "grant_type": 'client_credentials'
  }
  r = requests.post('https://id.twitch.tv/oauth2/token', body)
  #data output
  keys = r.json();
  
  headers = {
      'Client-ID': client_id,
      'Authorization': 'Bearer ' + keys['access_token']
  }
  
  stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)
  while stream.status_code!=200:
        print(f'Fixing twitch api error {stream.status_code} ...')
        time.sleep(5)
        stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)
  stream_data = stream.json();
  
  if len(stream_data['data']) == 1:
    #print(streamer_name + ' is live: ' + stream_data['data'][0]['title'] + ' playing ' + stream_data['data'][0]['game_name']);
    return True, stream_data["data"][0]['viewer_count'], stream_data["data"][0]['game_name']
  else:
    return False
    #print(streamer_name + ' is not live');

def check_streamer_existence(streamer_name):
    client_id = os.getenv('TWITCH_CLIENT_ID')
    client_secret = os.getenv('TWITCH_CLIENT_SECRET')

    body = {
      'client_id': client_id,
      'client_secret': client_secret,
      "grant_type": 'client_credentials'
  }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
  
    #data output
    keys = r.json();
  
    headers = {
      'Client-ID': client_id,
      'Authorization': 'Bearer ' + keys['access_token']
  }
  
    stream = requests.get('https://api.twitch.tv/helix/users?login=' + streamer_name, headers=headers)
    while stream.status_code!=200:
        print(f'Fixing twitch api error {stream.status_code} ...')
        time.sleep(5)
        stream = requests.get('https://api.twitch.tv/helix/users?login=' + streamer_name, headers=headers)

    stream_data = stream.json();
    if stream_data['data']==[]:
        return False
    else:
        return True