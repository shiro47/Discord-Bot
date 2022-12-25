import pymongo
from decouple import config

client = pymongo.MongoClient(f"mongodb+srv://shiro_47:{config('MONGODB_PASSWORD')}@gs-discord.y06kt.mongodb.net/?retryWrites=true&w=majority")
db = client["GS_Database"]


class twitch_db():
       
    def __init__(self):
        self.collection = db["TWITCH_DB"]
        
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
        if self.check_existance(streamer)==False:
            self.collection.delete_one({"streamer_name":streamer})
            return True
        return False
        
    def get_all_streamers(self):
        return self.collection.find()


class apex_db():
    
    def __init__(self):
        self.collection = db["APEX_DB"]
        
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
    
    
    