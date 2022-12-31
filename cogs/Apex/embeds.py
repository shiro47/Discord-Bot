from discord import app_commands
from discord.ext import commands, tasks
import datetime
import utilities

class ApexLegends_embeds(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.update_pred.start(971385355062370334, 971385734701387816)
        self.update_map_rotation.start(973284454376296538, 973284663885967431)

    @tasks.loop(hours=1)
    async def update_pred(self,channel_id,message_id):
        await self.bot.wait_until_ready()
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'| Updating predator threshold...')
        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.edit(embed=utilities.embed_pred(), content='')
        print(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), '| Predator threshold updated.')

    @tasks.loop(minutes=10)
    async def update_map_rotation(self,channel_id,message_id):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        print(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), '| Updating map rotation...')
        await message.edit(embed=utilities.embed_map_rotation(), content='')
        print(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), '| Map rotation updated.')
        
async def setup(bot :commands.Bot):
    await bot.add_cog(ApexLegends_embeds(bot))