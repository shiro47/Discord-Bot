import discord
from discord.ext import commands
from discord import app_commands
from decouple import config


class MyBot(commands.Bot):
    
    def __init__(self):
        super().__init__(command_prefix='>', intents=discord.Intents.all(), application_id=929089506316025907)
        
        self.initial_extansions = [
            "cogs.Apex.leaderboard",
            "cogs.Apex.embeds",
            "cogs.Twitch.streamers_live_list",
            "cogs.exception_handler",
        ]
    
        
    async def on_ready(self):
        IDs_leaderboard=[1054045651882737775,1054045666416013462,1054045682564083823,1054045744568487946,1054045761882575000,1054045774704541727,1054045853448413196]
        print(f'We have logged in as {self.user}')
        # apex.update_pred.start(971385355062370334,971385734701387816)
        # apex.update_map_rotation.start(973284454376296538,973284663885967431)
        # apex.update_leaderboard.start(971385355062370334,IDs_leaderboard)
        # twitch.update_ttv_category.start()
    
    async def setup_hook(self):
        for ext in self.initial_extansions:
            await self.load_extension(ext)
        await bot.tree.sync()


if __name__ == "__main__":
    bot = MyBot()
    bot.run(config('TOKEN'))
