import discord 
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
import datetime
import time
import utilities
from APIs.apex_api import Apex_API
import mongo_database


class ApexLegends_leaderboard(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.apex_db = mongo_database.apex_db()
        self.IDs_leaderboard = [1054045651882737775,1054045666416013462,1054045682564083823,1054045744568487946,1054045761882575000,1054045774704541727,1054045853448413196]
        self.update_leaderboard.start(971385355062370334,self.IDs_leaderboard)
        
    @app_commands.command(name = "help", description = "How to register to leaderboard",)
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed= utilities.embed_help())

    
    @app_commands.describe(platform= "Choose platform", nickname="Your origin nickname")
    @app_commands.choices(platform=[
        Choice(name="PC", value="PC"),
        Choice(name="PS", value="PS4"),
        Choice(name="XBOX", value="X1"),
                                    ])
    @app_commands.command(name = "register", description = "Register to Apex leaderboard.")
    async def register(self, interaction: discord.Interaction, platform: str, nickname: str):
        await interaction.response.defer()
        platforms=('PC','PS4','X1')
        if self.apex_db.check_existance(str(interaction.user.id))==False: 
            if platform in platforms:                   
                if Apex_API().get_rankScore(platform,nickname)!=None:
                    self.apex_db.add_player(platform, nickname, str(interaction.user.id))
                    await interaction.followup.send('Zarejestrowano.')
                else:
                    await interaction.followup.send('Prawidłowy zapis: `>register {platforma(PC,PS4,X1)} {nick origin}`')
            else:
                await interaction.followup.send('Źle wpisana platforma.')
        else:
            await interaction.followup.send('Jesteś już w systemie.')

    
    @app_commands.command(name = "unregister", description = "Unregister from Apex leaderboard.")
    async def unregister(self, interaction: discord.Interaction): 
        await interaction.response.defer()
        if self.apex_db.check_existance(str(interaction.user.id)):
            self.apex_db.remove_player(str(interaction.user.id))
            await interaction.followup.send('Wyrejestrowano.')
            return        
        await interaction.followup.send('Nie jesteś zarejestrowany.')



    

    @tasks.loop(hours=1)
    async def update_leaderboard(self, channel_id, message_IDs: dict):
        await self.bot.wait_until_ready()
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
        channel= self.bot.get_channel(channel_id)
        var=0
        players= await utilities.creating_rank_dict()
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
                    user= await self.bot.fetch_user(player)
                    player=self.apex_db.get_player(player)["ID"]
                    RP=y[1][1]
                    if x=='Apex Predator':
                        embed.add_field(name=str(pos)+f'**. {user.name}**', value=player+' | RP '+str(RP), inline=False)
                    else:
                        embed.add_field(name=str(pos)+f'**. {user.name}**', value='```'+player+' | '+f'{x} {y[1][2]}'+'\n'+utilities.rank_progress_bar(RP,x,y[1][2])+'```', inline=False)
                    pos+=1
            var+=1
            await message.edit(embed=embed,content='')
            time.sleep(3)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Leaderboard updated.')
        


async def setup(bot :commands.Bot):
    await bot.add_cog(ApexLegends_leaderboard(bot))