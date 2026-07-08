import discord
from discord.ext import commands
from discord import app_commands
from services.team_service import TeamService
from utils.premium import require_premium

class TeamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='team', description='View team recommendations for the selected animus.')
    @require_premium()
    async def team(self, interaction: discord.Interaction, animus: str):
        teams = TeamService.get_animus_teams(animus)
        
        if not teams:
            await interaction.response.send_message(
                "Animus not found."
            )
            return
        
        image_url = teams.get('image')
        team_data = teams.get('teams')
        color_data = teams.get('element')
        
        color_map = {
            'Red': discord.Color.red(),
            'Blue': discord.Color.blue(),
            'Green': discord.Color.green(),
            'Light': discord.Color.gold(),
            'Dark': discord.Color.purple()
        }

        embed = discord.Embed(title=f"{teams['name']} Teams", color=color_map.get(color_data))
        
        if image_url:
            embed.set_thumbnail(url=image_url or self.bot.user.display_avatar.url)
        
        for archetype, members in team_data.items():
            if not members:
                members = ["No team recommendations available."]
                
            embed.add_field(
                name = f"{archetype}:",
                value = ' | '.join(members),
                inline = False
            )
        
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(TeamCog(bot))