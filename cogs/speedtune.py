import discord
from discord.ext import commands
from discord import app_commands
from services.speed_service import SpeedService

class SpeedTuneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='speedtune', description='Recommend speed order.')
    async def speedtune(self, interaction: discord.Interaction, animus1: str, animus2: str, animus3: str, animus4: str):
        team = [
            animus1,
            animus2,
            animus3,
            animus4
        ]
        
        order = SpeedService.speed_order(team)
        
        embed = discord.Embed(title='Recommended Speed Order')
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        text = ""
        
        for idx, unit in enumerate(order, 1):
            text += f'{idx}. {unit['name']}\n'
        
        embed.description = text
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(SpeedTuneCog(bot))