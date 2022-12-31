import time
import json
import requests
from decouple import config

class Twitch_API():
    
    def __init__(self) -> None:
        self.client_id = config('TWITCH_CLIENT_ID')
        self.client_secret = config('TWITCH_CLIENT_SECRET')
    
    def check_stream_status(self, streamer_name):
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            "grant_type": 'client_credentials'
        }
        r = requests.post('https://id.twitch.tv/oauth2/token', body)
        #data output
        keys = r.json();
        
        headers = {
            'Client-ID': self.client_id,
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

    def check_streamer_existence(self, streamer_name):
        body = {
        'client_id': self.client_id,
        'client_secret': self.client_secret,
        "grant_type": 'client_credentials'
        }
        r = requests.post('https://id.twitch.tv/oauth2/token', body)
    
        #data output
        keys = r.json();
    
        headers = {
        'Client-ID': self.client_id,
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
    