import discord 
import datetime
from APIs.apex_api import Apex_API
from APIs.twitch_api import Twitch_API
from mongo_database import twitch_db as twitch_database
from mongo_database import apex_db as apex_database
from tqdm import tqdm
import json
import typing
import functools
import asyncio

twitch_db = twitch_database()
apex_db = apex_database()
twitch_api = Twitch_API()
apex_api = Apex_API()

def jprint(obj):        # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

def embed_help():
    embed= discord.Embed(title='Dostępne komendy ', timestamp= datetime.datetime.utcnow(), color=discord.Color.purple())
    embed.add_field(name="Zarejestrowanie do leaderboard'a", value='`/register {platforma(PC,PS4,X1)} {nick origin}`', inline=False)
    embed.add_field(name="Wyrejestrowanie", value='`/unregister`', inline=False)
    return embed

def embed_pred():
    values=apex_api.pred_threshold()
    embed = discord.Embed(title='BR Predator Threshold: '+str(values[0])+' RP\n`Total Masters and Preds:` '+str(values[1])+' \n\nArena Predator Threshold: '+str(values[2])+' RP\n`Total Masters and Preds:` '+str(values[3]), color=discord.Color.dark_red(),timestamp= datetime.datetime.utcnow())
    embed.set_thumbnail(url="https://api.mozambiquehe.re/assets/ranks/apexpredator1.png")
    return embed

@to_thread
def creating_rank_dict():
    players={}
    for player in apex_db.get_all_players():
        playerID=player['DiscordID']
        platform1=player['platform']
        players.update({playerID:apex_api.get_rankScore(platform1,player['ID'])})                   
    return players

def embed_map_rotation():
    values=apex_api.map_rotation_data()
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



def rank_progress_bar(RP,rank, rank_division):
    if rank=='Master':
        pred_rp=apex_api.pred_threshold()[0]
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

@to_thread
def create_streamers_list():
    streamers={}
    for x in twitch_db.get_all_streamers():
            for streamer in x.items():
                if streamer[0]=='streamer_name':
                    status=twitch_api.check_stream_status(streamer[1])
                    if status!=False:
                        streamers.update({streamer[1]: [status[1],status[2]]})
                    else:
                        continue
    return streamers

def embed_all_streamers():
    embed = discord.Embed(title="Registered streamers in database:" ,color=discord.Color.dark_purple(),timestamp= datetime.datetime.utcnow())
    text="```"
    pos=1
    for streamer in twitch_db.get_all_streamers():
        text+=f"{str(pos)}. {streamer['streamer_name']}\n"
        pos+=1
    text+="```"
    embed.add_field(name="\u200b", value=text)
    return embed

def is_owner(interaction: discord.Interaction):
    if interaction.user.id == 33253250299015987:
        return True
    return False

