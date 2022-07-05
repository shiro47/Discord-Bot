import functions
import dc_functions
import discord
import os 
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import datetime
import asyncio
from tinydb import TinyDB, Query

db = TinyDB('db.json')
twitch_db = TinyDB('twitch_db.json')
user = Query()


load_dotenv()


bot = commands.Bot(command_prefix=">", help_command=None)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error




##############################################################TWITCH########################################################################

@bot.command()
@commands.has_any_role(683637694903222382, 862315076346052628)
async def register_ttv(ctx, streamer):
    if functions.check_streamer_existence(streamer)==True:
        if twitch_db.search(user.streamer_name == streamer)==[]:
            twitch_db.insert({'streamer_name': streamer})
            await ctx.send("Zarejestrowano streamera.")
        else:
            await ctx.send("Streamer już istnieje.")

    else:
        await ctx.send(f"Streamer {streamer} nie istnieje.")

@bot.command()
@commands.has_any_role(683637694903222382, 862315076346052628)
async def unregister_ttv(ctx, streamer):
    if twitch_db.search(user.streamer_name == streamer)==[]:
        await ctx.send(f"Streamer {streamer} nie jest zarejestrowany.")
    else: 
        twitch_db.remove(user.streamer_name==streamer)
        await ctx.send("Wyrejestrowano streamera.")

@bot.command()
@commands.has_any_role(683637694903222382, 862315076346052628)
async def setup_ttv_category(ctx):
    try:
        await ctx.send("Setting up management!")
        await ctx.guild.create_category( "🎥 ONLINE STREAMERS 🎥", overwrites=None, reason=None)
        await ctx.send("Setup finished!")
    except Exception as errors:
        print(f"Bot Error: {errors}")

@bot.command(pass_context=True)
@commands.has_any_role(683637694903222382, 862315076346052628)
async def del_category(ctx, category: discord.CategoryChannel):
    delcategory = category # delcategory is our ID (category)
    channels = delcategory.channels # Get all channels of the category
    for channel in channels: # We search for all channels in a loop
        try:
            await channel.delete() # Delete all channels
        except AttributeError: # If the category does not exist/channels are gone
            pass
    await delcategory.delete() # At the end we delete the category, if the loop is over

@bot.command()
@commands.has_any_role(683637694903222382, 862315076346052628)
async def update_ttv_category():
    while True:
        category= bot.get_channel(993829164392132668)
        delcategory = category
        channels = delcategory.channels # Get all channels of the category
        for channel in channels: # We search for all channels in a loop
            try:
                await channel.delete() # Delete all channels
            except AttributeError: # If the category does not exist/channels are gone
                pass
        
        try:
            guild = bot.get_guild(610920227085221898) # <-- insert yor guild id here
            streamers= dc_functions.create_streamers_list()
            streamers=sorted(streamers.items(), key=lambda x: x[1], reverse=True)
            cut_nicknames={"tsm_imperialhal":"imperial", "sweetdreams":"sweet", "diegosaurs":"diego" }
            for streamer in streamers:
                if streamer[0] in cut_nicknames:
                    await guild.create_voice_channel(f"🟢  {cut_nicknames[streamer[0]].upper()}  👤: ≈ {streamer[1]}", overwrites=None, category=category, reason=None)
                else:
                    await guild.create_voice_channel(f"🟢  {streamer[0].upper()}  👤: ≈ {streamer[1]}", overwrites=None, category=category, reason=None)
        except Exception as errors:
            print(f"Bot Error: {errors}")
        await asyncio.sleep(510)

###################################################################APEX LEGENDS###################################################################

@bot.command()
async def help(ctx):
    await ctx.send(embed= dc_functions.embed_help())

@bot.command()
async def register(ctx, *args):
    platforms=('PC','PS4','X1')
    platform=None
    nickname=None
    if ctx.author==bot.user:
        return
    if len(args)==2:
        if db.search(user.DiscordID == str(ctx.author.id))==[]:                    
            if args[0] in platforms:
                platform=args[0]
                nickname=args[1]
                if functions.get_rankScore(platform,nickname)!=None:
                    db.insert({'platform': platform, 'ID': nickname, 'DiscordID': str(ctx.author.id)})
                    await ctx.send('Zarejestrowano.')
                else:
                    await ctx.send('Źle wprowadzony nick.')
            else:
                await ctx.send('Źle wprowadzona platforma.')
        else:
            await ctx.send('Jesteś już w systemie.')
    else:
        await ctx.send('Prawidłowy zapis: `>register {platforma(PC,PS4,X1)} {nick origin}`')

@bot.command()
async def unregister(ctx, *args):
    if ctx.author==bot.user:
        return    
    db.remove(user.DiscordID==str(ctx.author.id))
    await ctx.send('Wyrejestrowano.')        

@bot.command()
@commands.has_any_role(683637694903222382, 862315076346052628)
async def update_pred(channel_id,message_id):
    while True:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Updating predator threshold...')
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.edit(embed=dc_functions.embed_pred(),content='')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Predator threshold updated.')
        await asyncio.sleep(3600)

@bot.command()
@commands.has_any_role(683637694903222382, 862315076346052628)
async def update_map_rotation(channel_id,message_id):
    while True:
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Updating map rotation...')
        await message.edit(embed=dc_functions.embed_map_rotation(), content='')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Map rotation updated.')
        await asyncio.sleep(600)

IDs_leaderboard=[972863566669574185,972863568326303804,972863574701670500,972863576270340177,972863577851580416,972863589138448444,972863590354804756]

@bot.command()
@commands.has_any_role(683637694903222382, 862315076346052628)
async def update_leaderboard(channel_id, message_IDs: dict):
    while True:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Updating leaderboard...')
        ranks=('Apex Predator','Master','Diamond','Platinum','Gold','Silver','Bronze')
        IDs=message_IDs
        channel= bot.get_channel(channel_id)
        var=0
        players=dc_functions.creating_rank_dict()
        players=sorted(players.items(), key=lambda x: x[1][1], reverse=True)
        for x in ranks:        
            message = await channel.fetch_message(IDs[var])
            embed = discord.Embed(title=f"__**{x}**__", timestamp= datetime.datetime.utcnow())
            if x=='Apex Predator':
                embed.set_thumbnail(url="https://api.mozambiquehe.re/assets/ranks/apexpredator1.png")
            else:
                embed.set_thumbnail(url="https://api.mozambiquehe.re/assets/ranks/{rank}.png".format(rank=x.casefold()))
            pos=1
            for y in players:
                if y[1][0]==x:
                    player=y[0]
                    RP=y[1][1]
                    user = await bot.fetch_user(dc_functions.get_discordID(player))
                    embed.add_field(name=str(pos)+f'**. {user}**', value=player+' | RP '+str(RP), inline=False)
                    pos+=1
            var+=1
            await message.edit(embed=embed,content='')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Leaderboard updated.')
        await asyncio.sleep(3600)
    

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    asyncio.create_task(update_pred(971385355062370334,971385734701387816))
    asyncio.create_task(update_map_rotation(973284454376296538,973284663885967431))
    asyncio.create_task(update_leaderboard(971385355062370334,IDs_leaderboard))
    asyncio.create_task(update_ttv_category())



bot.run(os.getenv('TOKEN'))