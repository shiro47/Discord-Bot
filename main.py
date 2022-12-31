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
        print(f'We have logged in as {self.user}')
    
    
    async def setup_hook(self):
        for ext in self.initial_extansions:
            await self.load_extension(ext)
        await bot.tree.sync()


if __name__ == "__main__":
    bot = MyBot()
    bot.run(config('TOKEN'))
