import discord 
import datetime
import API_functions
from tinydb import TinyDB, Query
from tqdm import tqdm

db = TinyDB('db/db.json')
twitch_db = TinyDB('db/twitch_db.json')
user = Query()

def embed_pred():
    values=API_functions.pred_threshold()
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
                players.update({player:API_functions.get_rankScore(platform1,player)})                   
    return players

def create_streamers_list():
    streamers={}
    for x in iter(twitch_db):
            for streamer in x.items():
                if streamer[0]=='streamer_name':
                    status=API_functions.check_stream_status(streamer[1])
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
    values=API_functions.map_rotation_data()
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


def rank_progress_bar(RP,rank, rank_division):
    if rank=='Master':
        pred_rp=API_functions.pred_threshold()[0]
        return tqdm.format_meter(RP-15000,pred_rp-15000,0,bar_format='{desc} RP  |{bar}|  {postfix} RP', ncols=40, prefix=f"{RP}", postfix=pred_rp )
    ranks = {
        'Diamond': [11400, 12300, 13200, 14100],
        'Platinum': [8200, 9000, 9800, 10600],
        'Gold': [5400, 6100, 6800, 7500],
        'Silver': [3000, 3600, 4200, 4800],
        'Bronze': [1000, 1500, 2000, 2500]
    }
    rank_divisions={
        4:0,
        3:1,
        2:2,
        1:3,
        }
    total_rank_rp = ranks[rank][1]-ranks[rank][0]
    for n in rank_divisions:
        if n==rank_division:
            rank_number=rank_divisions[n]
    return tqdm.format_meter(RP-ranks[rank][rank_number],total_rank_rp,0,bar_format='{desc} RP  |{bar}|  {postfix} RP', ncols=40, prefix=f"{RP}", postfix=ranks[rank][rank_number]+total_rank_rp)

