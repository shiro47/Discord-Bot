import discord 
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
import datetime
import dc_functions
import API_functions
import mongo_database




class Twitch_live_list(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.twitch_db = mongo_database.twitch_db()
        
    @app_commands.checks.has_any_role(683637694903222382)
    @app_commands.describe(streamer= "Streamer nickname")
    @app_commands.command(name = "register_ttv", description = "Register twitch streamer to database.")
    async def register_ttv(self, interaction: discord.Interaction, streamer: str):
        await interaction.response.defer()
        if API_functions.check_streamer_existence(streamer)==True:
            if self.twitch_db.check_existance(streamer)==False:
                self.twitch_db.add_streamer(streamer)
            else:
                await interaction.followup.send(f"Streamer {streamer} już istnieje w bazie danych.")
                return
        else:
            await interaction.followup.send(f"Streamer {streamer} nie istnieje.")
            return
        await interaction.followup.send("Zarejestrowano pomyślnie.")
    
    @app_commands.describe(streamer= "Streamer nickname")
    @app_commands.command(name = "unregister_ttv", description = "Unregister twitch streamer from database.")
    @app_commands.checks.has_any_role(683637694903222382, 862315076346052628)
    async def unregister_ttv(self, interaction: discord.Interaction, streamer: str):
        await interaction.response.defer()
        if self.twitch_db.check_existance(streamer)==False:
            await interaction.followup.send(f"Streamer {streamer} nie jest zarejestrowany.")
        else: 
            self.twitch_db.remove_streamer(streamer)
            await interaction.followup.send("Wyrejestrowano streamera.")
            
    @app_commands.command(name = "registered_streamers", description = "Display registered streamers in database.")
    @app_commands.checks.has_any_role(683637694903222382, 862315076346052628)
    async def registered_streamers(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(embed = dc_functions.embed_all_streamers())
    
    # @app_commands.command()
    # @commands.has_any_role(683637694903222382, 862315076346052628)
    # async def setup_ttv_category(self, ctx):
    #     try:
    #         await ctx.send("Setting up management!")
    #         await ctx.guild.create_category( "🎥 ONLINE STREAMERS 🎥", overwrites=None, reason=None)
    #         await ctx.send("Setup finished!")
    #     except Exception as errors:
    #         print(f"Bot Error: {errors}")

    # @app_commands.command()
    # @commands.has_any_role(683637694903222382, 862315076346052628)
    # async def del_category(ctx, category: discord.CategoryChannel):
    #     delcategory = category # delcategory is our ID (category)
    #     channels = delcategory.channels # Get all channels of the category
    #     for channel in channels: # We search for all channels in a loop
    #         try:
    #             await channel.delete() # Delete all channels
    #         except AttributeError: # If the category does not exist/channels are gone
    #             pass
    #     await delcategory.delete() # At the end we delete the category, if the loop is over


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
        guild = self.bot.get_guild(610920227085221898)  # <-- insert yor guild id here

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
            category_id = self.bot.get_channel(categories[category][0])
            channels = category_id.channels  # Get all channels of the category
            for channel in channels:  # We search for all channels in a loop
                try:
                    await channel.delete()  # Delete all channels
                except AttributeError:  # If the category does not exist/channels are gone
                    pass
            
            channel = self.bot.get_channel(1002582923121274890)
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
            
            
async def setup(bot :commands.Bot):
    await bot.add_cog(Twitch_live_list(bot))