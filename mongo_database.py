import pymongo
from decouple import config

client = pymongo.MongoClient(f"mongodb+srv://shiro_47:{config('MONGODB_PASSWORD')}@gs-discord.y06kt.mongodb.net/?retryWrites=true&w=majority")


class config_db():
    
    def __init__(self, server_id):
        self.server= client[server_id]
        self.collection = self.server["CONFIG"]

    def create_ids_for_map_rotation(self,channel_id, message_id, message_id_ranked):
        data={
                "Name":"Map_rotation",
                "channel_id":channel_id, 
                "message_id":message_id,
                "message_id_ranked":message_id_ranked
            }
        if not self.collection.find_one({"Name":"Map_rotation"}):
            self.collection.insert_one(data)
        else:
            self.collection.delete_one({"Name":"Map_rotation"})
            self.collection.insert_one(data)
            
    def create_ids_for_pred(self, channel_id, message_id):
        data={
            "Name":"Predator_embed",
            "channel_id":channel_id, 
            "message_id":message_id
        }
        if not self.collection.find_one({"Name":"Predator_embed"}):
            self.collection.insert_one(data)
        else:
            self.collection.delete_one({"Name":"Predator_embed"})
            self.collection.insert_one(data)
        
    def create_ids_for_apex_leaderboard(self,channel_id,IDs: list):
        data={
            "Name":"Leaderbord_IDs",
            "channel_id":channel_id,
            "message_ids":IDs
        }
        if not self.collection.find_one({"Name":"Leaderbord_IDs"}):
            self.collection.insert_one(data)
        else:
            self.collection.delete_one({"Name":"Leaderbord_IDs"})
            self.collection.insert_one(data)
            
    def create_ids_for_streams_list(self,channel_id):
        data={
                "Name":"Streams_list",
                "channel_id":channel_id, 
        }
        if not self.collection.find_one({"Name":"Streams_list"}):
            self.collection.insert_one(data)
        else:
            self.collection.delete_one({"Name":"Streams_list"})
            self.collection.insert_one(data)
            
    def check_ids_for_map_rotation(self):
        data = self.collection.find_one({"Name":"Map_rotation"})
        if not data: 
            return False
        return data 
    
    def check_ids_for_pred(self):
        data = self.collection.find_one({"Name":"Predator_embed"})
        if not data: 
            return False
        return data
    
    def check_ids_for_apex_leaderboard(self):
        data = self.collection.find_one({"Name":"Leaderbord_IDs"})
        if not data: 
            return False
        return data
    
    def check_ids_for_streams_list(self):
        data = self.collection.find_one({"Name":"Streams_list"})
        if not data: 
            return False
        return data 
    
class twitch_db():
       
    def __init__(self, server_id):
        self.server= client[server_id]
        self.collection = self.server["TWITCH_DB"]
        
        
    def check_existance(self, streamer):
        if self.collection.find_one({"streamer_name":streamer})!=None:
            return True
        return False
    
    def add_streamer(self, streamer):
        if self.check_existance(streamer)==False:
            self.collection.insert_one({"streamer_name":streamer.lower()})
            return True
        return False
    
    def remove_streamer(self, streamer):
        if self.check_existance(streamer)==True:
            self.collection.delete_one({"streamer_name":streamer})
            return True
        return False
        
    def get_all_streamers(self):
        return self.collection.find()


class apex_db():
    
    def __init__(self, server_id):
        self.server= client[server_id]
        self.collection = self.server["APEX_DB"]
        
    def check_existance(self, discordID):
        if self.collection.find_one({"DiscordID":discordID})!=None:
            return True
        return False            
    
    def add_player(self, platform, nickname, discordID):
        if self.check_existance(discordID)==False:
            self.collection.insert_one({'platform': platform, 'ID': nickname, 'DiscordID': discordID})
            return True
        return False
    
    def remove_player(self, discordID):
        if self.check_existance(discordID)==True:
            self.collection.delete_one({"DiscordID": discordID})
            return True
        return False
    
    def get_all_players(self):
        return self.collection.find()
    
    def get_player(self, discordID):
        if self.check_existance(discordID)==True:
            return self.collection.find_one({"DiscordID":discordID})
        return False
    
    
    