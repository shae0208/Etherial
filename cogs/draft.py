import discord
from discord.ext import commands
from discord import app_commands
from services.draft_service import DraftService

class DraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='draft', description='Recommend draft bans.')
    async def draft(self, interaction: discord.Interaction, animus1: str, animus2: str, animus3: str, animus4: str, animus5: str):
        enemy_team = [
            animus1,
            animus2,
            animus3,
            animus4,
            animus5
        ]
        
        ban = DraftService.recommend_ban(enemy_team, protected_indices={2})
        
        embed = discord.Embed(title='Draft Assistant')
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        embed.add_field(
            name = 'Enemy Draft',
            value = '\n'.join(DraftService.format_team(enemy_team)),
            inline = False
        )
        embed.add_field(
            name = 'Recommended Ban',
            value = ban or 'No recommendation available',
            inline = False
        )
        
        await interaction.response.send_message(embed = embed)
        
async def setup(bot):
    await bot.add_cog(DraftCog(bot))