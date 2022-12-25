import discord
from discord.ext import commands
from discord import app_commands

class ExceptionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, interaction: discord.Interaction, error) -> None:
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message("Sorry, you do not have permission to do this!")
        else:
            raise error
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExceptionHandler(bot))