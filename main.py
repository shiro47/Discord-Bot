import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from discord import app_commands
import API_functions
import dc_functions
from mongo_database import twitch_db as twitch_database
from mongo_database import apex_db as apex_database
import datetime
from decouple import config
import time


twitch_db=twitch_database()
apex_db=apex_database()


intents = discord.Intents(messages=True, guilds=True)
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error
    
@tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id ==332532502990159873:
        await tree.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')
##############################################################TWITCH########################################################################

class Twitch_module():
    
    @tree.command()
    @commands.has_any_role(683637694903222382, 862315076346052628)
    async def register_ttv(ctx, *args):
        for streamer in args:
            if API_functions.check_streamer_existence(streamer)==True:
                if twitch_db.check_existance(streamer)==False:
                    twitch_db.add_streamer(streamer)
                else:
                    await ctx.send(f"Streamer {streamer} już istnieje w bazie danych.")
            else:
                await ctx.send(f"Streamer {streamer} nie istnieje.")
        await ctx.send("Zarejestrowano pomyślnie.")

    @tree.command()
    @commands.has_any_role(683637694903222382, 862315076346052628)
    async def unregister_ttv(ctx, streamer):
        if twitch_db.check_existance(streamer)==False:
            await ctx.send(f"Streamer {streamer} nie jest zarejestrowany.")
        else: 
            twitch_db.remove_streamer(streamer)
            await ctx.send("Wyrejestrowano streamera.")
            
    @tree.command()
    @commands.has_any_role(683637694903222382, 862315076346052628)
    async def registered_streamers(self, ctx):
        await ctx.send(embed = dc_functions.embed_all_streamers())
    
    @tree.command()
    @commands.has_any_role(683637694903222382, 862315076346052628)
    async def setup_ttv_category(self, ctx):
        try:
            await ctx.send("Setting up management!")
            await ctx.guild.create_category( "🎥 ONLINE STREAMERS 🎥", overwrites=None, reason=None)
            await ctx.send("Setup finished!")
        except Exception as errors:
            print(f"Bot Error: {errors}")

    @tree.command()
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


    @tasks.loop(minutes=8)
    async def update_ttv_category(self):
        categories = {
                    "Apex Legends": [993829164392132668,1002583106252972032, 'https://static-cdn.jtvnw.net/ttv-boxart/511224-285x380.jpg', discord.Color.dark_red()],
                    "Just Chatting": [994278145509310485, 1002583145553596416,'https://static-cdn.jtvnw.net/ttv-boxart/509658-285x380.jpg', discord.Color.from_rgb(201, 199, 191)],
                    "Phasmophobia": [994279106210439238, 1002583186188025857, 'https://static-cdn.jtvnw.net/ttv-boxart/518184_IGDB-285x380.jpg', discord.Color.from_rgb(36, 35, 34)],
                    "VALORANT": [994279798484516905, 1002583252441247924, 'https://static-cdn.jtvnw.net/ttv-boxart/516575-285x380.jpg', discord.Color.from_rgb(252, 40, 51)],
                    "League of Legends": [994280414686498937, 1002583268518010991, 'https://static-cdn.jtvnw.net/ttv-boxart/21779-285x380.jpg', discord.Color.from_rgb(1, 110, 32)],
                    }
        cut_nicknames = {"tsm_imperialhal": "imperial", "sweetdreams": "sweet", "diegosaurs": "diego", "Alliance_Hakis": "hakis", "EnemyAPEX": "enemy",
                        "YoungMulti": "Multi", "Pago3": "pago", "IzakOOO": "izak", "parisplatynov": "parisplat", "mrs_nocka": "nocka", "btyr3kt": "r3kt"}
        streamers = dc_functions.create_streamers_list()
        guild = bot.get_guild(610920227085221898)  # <-- insert yor guild id here

        for category in categories:
            streamers_by_category = {}
            # <-- Updating streamers_by_category with viewers count
            for streamer in list(streamers):
                if streamers[streamer][1] == category:
                    streamers_by_category.update(
                        {streamer: streamers[streamer][0]})
                    del streamers[streamer]
                elif streamers[streamer][1] not in categories and category == "Just Chatting":
                    streamers_by_category.update(
                        {streamer: streamers[streamer][0]})
                    del streamers[streamer]
                else:
                    continue
            streamers_by_category = sorted(
                streamers_by_category.items(), key=lambda x: x[1], reverse=True)
            category_id = bot.get_channel(categories[category][0])
            channels = category_id.channels  # Get all channels of the category
            for channel in channels:  # We search for all channels in a loop
                try:
                    await channel.delete()  # Delete all channels
                except AttributeError:  # If the category does not exist/channels are gone
                    pass
            
            channel = bot.get_channel(1002582923121274890)
            message = await channel.fetch_message(categories[category][1])
            embed = discord.Embed(title=f"__**{category}**__", timestamp= datetime.datetime.utcnow(), color=categories[category][3])
            embed.set_thumbnail(url=f'{categories[category][2]}')
            
            pos=1
            for streamer in streamers_by_category:
                try:
                    if streamer[0] in cut_nicknames:
                        await guild.create_voice_channel(f"🟢  {cut_nicknames[streamer[0]].upper()}  👤: ≈ {streamer[1]}", overwrites=None, category=category_id, reason=None)
                        embed.add_field(name=f'{pos}. 🟢 {cut_nicknames[streamer[0]].capitalize()} \n👤: ≈ {streamer[1]}', value=f'https://www.twitch.tv/{streamer[0].casefold()}', inline=False)
                        pos+=1
                    else:
                        await guild.create_voice_channel(f"🟢  {streamer[0].upper()}  👤: ≈ {streamer[1]}", overwrites=None, category=category_id, reason=None)
                        embed.add_field(name=f'{pos}. 🟢 {streamer[0].capitalize()} \n👤: ≈ {streamer[1]}', value=f'https://www.twitch.tv/{streamer[0].casefold()}', inline=False)
                        pos+=1
                except Exception as errors:
                    print(f"Bot Error: {errors}")
            await message.edit(embed=embed,content='')


###################################################################APEX LEGENDS###################################################################

class ApexLegends_module():

    @tree.command(name = "help", description = "How to register to leaderboard",)
    async def help(self, interaction):
        await interaction.response.send_message("Hello!")
        #send(embed= dc_functions.embed_help())

    @tree.command()
    async def register(ctx, *args):
        platforms=('PC','PS4','X1')
        platform=None
        nickname=None
        if ctx.author==bot.user:
            return
        if len(args)==2:
            if apex_db.check_existance(str(ctx.author.id))==False:                    
                if args[0] in platforms:
                    platform=args[0]
                    nickname=args[1]
                    if API_functions.get_rankScore(platform,nickname)!=None:
                        apex_db.add_player(platform, nickname, str(ctx.author.id))
                        await ctx.send('Zarejestrowano.')
                    else:
                        await ctx.send('Źle wprowadzony nick.')
                else:
                    await ctx.send('Źle wprowadzona platforma.')
            else:
                await ctx.send('Jesteś już w systemie.')
        else:
            await ctx.send('Prawidłowy zapis: `>register {platforma(PC,PS4,X1)} {nick origin}`')

    @tree.command()
    async def unregister(ctx, *args):
        if ctx.author==bot.user:
            return    
        if apex_db.remove_player(str(ctx.author.id)):
            await ctx.send('Wyrejestrowano.')
            return        
        await ctx.send('Nie jesteś zarejestrowany.')


    @tasks.loop(hours=1)
    async def update_pred(self,channel_id,message_id):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Updating predator threshold...')
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.edit(embed=dc_functions.embed_pred(), content='')
        print(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), '| Predator threshold updated.')



    @tasks.loop(minutes=10)
    async def update_map_rotation(self,channel_id,message_id):
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        print(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), '| Updating map rotation...')
        await message.edit(embed=dc_functions.embed_map_rotation(), content='')
        print(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), '| Map rotation updated.')
    

    @tasks.loop(hours=1)
    async def update_leaderboard(self, channel_id, message_IDs: dict):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Updating leaderboard...')
        ranks={
                'Apex Predator': discord.Color.dark_red(),
            'Master':discord.Color.purple(),
            'Diamond':discord.Color.dark_blue(),
            'Platinum':discord.Color.blue(),
            'Gold':discord.Color.from_rgb(199, 158, 12),
            'Silver':discord.Color.light_grey(),
            'Bronze':discord.Color.from_rgb(184, 115, 51),
            }
        IDs=message_IDs
        channel= bot.get_channel(channel_id)
        var=0
        players=dc_functions.creating_rank_dict()
        players=sorted(players.items(), key=lambda x: x[1][1], reverse=True)
        for x in ranks:        
            message = await channel.fetch_message(IDs[var])
            embed = discord.Embed(title=f"__**{x}**__", timestamp= datetime.datetime.utcnow(), color=ranks[x])
            if x=='Apex Predator':
                embed.set_thumbnail(url="https://api.mozambiquehe.re/assets/ranks/apexpredator1.png")
            else:
                embed.set_thumbnail(url="https://api.mozambiquehe.re/assets/ranks/{rank}.png".format(rank=x.casefold()))
            pos=1
            for y in players:
                if y[1][0]==x:
                    player=y[0]
                    user= await bot.fetch_user(player)
                    player=apex_db.get_player(player)["ID"]
                    RP=y[1][1]
                    if x=='Apex Predator':
                        embed.add_field(name=str(pos)+f'**. {user.name}**', value=player+' | RP '+str(RP), inline=False)
                    else:
                        embed.add_field(name=str(pos)+f'**. {user.name}**', value='```'+player+' | '+f'{x} {y[1][2]}'+'\n'+dc_functions.rank_progress_bar(RP,x,y[1][2])+'```', inline=False)
                    pos+=1
            var+=1
            await message.edit(embed=embed,content='')
            time.sleep(3)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Leaderboard updated.')
    

@bot.event
async def on_ready():
    IDs_leaderboard=[1054045651882737775,1054045666416013462,1054045682564083823,1054045744568487946,1054045761882575000,1054045774704541727,1054045853448413196]
    print('We have logged in as {0.user}'.format(bot))
    # apex.update_pred.start(971385355062370334,971385734701387816)
    # apex.update_map_rotation.start(973284454376296538,973284663885967431)
    # apex.update_leaderboard.start(971385355062370334,IDs_leaderboard)
    # twitch.update_ttv_category.start()
if __name__ == "__main__":
    twitch=Twitch_module()
    apex = ApexLegends_module()
    bot.run(config('TOKEN'))
