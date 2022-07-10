import discord 
import datetime
import functions
from tinydb import TinyDB, Query

db = TinyDB('db/db.json')
twitch_db = TinyDB('db/twitch_db.json')
user = Query()

def embed_pred():
    values=functions.pred_threshold()
    embed = discord.Embed(title='BR Predator Threshold: '+str(values[0])+' RP\n`Total Masters and Preds:` '+str(values[1])+' \n\nArena Predator Threshold: '+str(values[2])+' RP\n`Total Masters and Preds:` '+str(values[3]), color=discord.Color.dark_red(),timestamp= datetime.datetime.utcnow())
    embed.set_thumbnail(url="https://cdn.apexstats.dev/ProjectRanked/Badges/Predator.png")
    return embed

def creating_rank_dict():
    platform1=None
    player=None
    players={}
    for y in iter(db):
            for t in y.items():
                if t[0]=='platform':
                    platform1=t[1]
                if t[0]=='ID':
                    player=t[1]
            if platform1!=None and player!=None:
                players.update({player:functions.get_rankScore(platform1,player)})                   
    return players

def create_streamers_list():
    streamers={}
    for x in iter(twitch_db):
            for streamer in x.items():
                if streamer[0]=='streamer_name':
                    status=functions.check_stream_status(streamer[1])
                    if status!=False:
                        streamers.update({streamer[1]: [status[1],status[2]]})
                    else:
                        continue
    return streamers


def get_discordID(gameID):
    for x in db.search(user.ID == gameID):
        for y in x.items():
            if y[0]=='DiscordID':
                return y[1]

def embed_map_rotation():
    values=functions.map_rotation_data()
    embed = discord.Embed(title=f'Aktualna mapa to: `{values[0]}`', timestamp= datetime.datetime.utcnow())
    if len(values[0].split())>1:
        word=values[0].split()
        map='_'.join(word)
        embed.set_image(url=f'https://apexlegendsstatus.com/assets/maps/{map}.png')
    else:
        embed.set_image(url=f'https://apexlegendsstatus.com/assets/maps/{values[0]}.png')
    embed.add_field(name='Pozostały czas: ', value=f'`{values[1]}`',inline=False)
    embed.add_field(name='Następna mapa: ', value=f'`{values[2]}`', inline=False)
    time = datetime.datetime.strptime(values[3], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
    embed.add_field(name='Start: ', value=f'`{time.strftime("%H:%M:%S")}`')
    time = datetime.datetime.strptime(values[4], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
    embed.add_field(name='Koniec: ', value=f'`{time.strftime("%H:%M:%S")}`')
    return embed

def embed_help():
    embed= discord.Embed(title='Dostępne komendy ', timestamp= datetime.datetime.utcnow(), color=discord.Color.purple())
    embed.add_field(name="Zarejestrowanie do leaderboard'a", value='`>register {platforma(PC,PS4,X1)} {nick origin}`', inline=False)
    embed.add_field(name="Wyrejestrowanie", value='`>unregister`', inline=False)
    return embed