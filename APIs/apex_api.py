import time
import json
import requests
from decouple import config

class Apex_API():
    def __init__(self) -> None:
        self.token=config('APEX_TOKEN')
    
    def pred_threshold(self):
        www2=requests.get(f'https://api.mozambiquehe.re/predator?auth={self.token}')
        if www2.status_code!=200:
            print(f'Fixing error {www2.status_code}...')
            time.sleep(5)
            return self.pred_threshold()
        if www2.status_code==200:
            try:
                parsed_json = (json.dumps(www2.json()))
                BR_info = (json.loads(parsed_json)["RP"]["PC"])
                ARENA_info = (json.loads(parsed_json)["AP"]["PC"])
            except KeyError:
                time.sleep(5)
                return self.pred_threshold()
            return BR_info['val'], BR_info['totalMastersAndPreds'], ARENA_info['val'], ARENA_info['totalMastersAndPreds']

    def get_rankScore(self,platform,player):
        www2=requests.get(f'https://api.mozambiquehe.re/bridge?auth={self.token}&player={player}&platform={platform}')
        if www2.status_code!=200:
            print(f'Fixing error {www2.status_code}...')
            time.sleep(5)
            return self.get_rankScore(platform,player)
        if www2.status_code==200:
            try:
                parsed_json=(json.dumps(www2.json()))
                player_rank_info=(json.loads(parsed_json)["global"]["rank"])
            except KeyError:
                time.sleep(5)
                return self.get_rankScore(platform,player)
            return player_rank_info['rankName'], player_rank_info['rankScore'], player_rank_info['rankDiv']


    def map_rotation_data(self):
        www2=requests.get(f'https://api.mozambiquehe.re/maprotation?auth={self.token}')
        if www2.status_code!=200:
            print(f'Fixing error {www2.status_code}...')
            time.sleep(5)
            return self.map_rotation_data()
        if www2.status_code==200:
            try:
                parsed_json=(json.dumps(www2.json()))
                current_map_info=(json.loads(parsed_json)["current"])
                next_map_info=(json.loads(parsed_json)["next"])
            except KeyError:
                time.sleep(5)
                return self.map_rotation_data()
            return current_map_info['map'], current_map_info['remainingTimer'], next_map_info['map'], next_map_info['readableDate_start'], next_map_info['readableDate_end']