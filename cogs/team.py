import discord
from discord.ext import commands
from discord import app_commands
from services.team_service import TeamService
from utils.premium import require_premium

class TeamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='team', description='View recommended teams.')
    async def team(self, interaction: discord.Interaction, animus: str):
        teams = TeamService.get_teams(animus)
        
        if not teams:
            await interaction.response.send_message(
                "Animus not found."
            )
            return
        
        embed = discord.Embed(title=f"{teams['name']} Teams")
        image_url = teams.get('image')
        team_data = teams.get('teams')
        
        if image_url:
            embed.set_thumbnail(url=image_url)
        
        for archetype, members in team_data.items():
            embed.add_field(
                name = archetype,
                value = '\n'.join(members),
                inline = True
            )
        
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(TeamCog(bot))