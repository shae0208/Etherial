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
        teams = TeamService.get_animus_teams(animus)
        
        if not teams:
            await interaction.response.send_message(
                "Animus not found."
            )
            return
        
        embed = discord.Embed(title=f"{teams['name']} Teams")
        image_url = teams.get('image')
        team_data = teams.get('teams')
        color_data = teams.get('element')
        
        if image_url:
            embed.set_thumbnail(url=image_url)
        
        if color_data == 'Red':
            embed.color = discord.Color.red()
        elif color_data == 'Blue':
            embed.color = discord.Color.blue()
        elif color_data == 'Green':
            embed.color = discord.Color.green()
        elif color_data == 'Light':
            embed.color = discord.Color.gold()
        elif color_data == 'Dark':
            embed.color = discord.Color.purple()
            
        for archetype, members in team_data.items():
            embed.add_field(
                name = archetype,
                value = ' | '.join(members),
                inline = False
            )
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name='test', description='Test premium features')
    @require_premium()
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Premium is working as intended",
            ephemeral = True
        )
    
async def setup(bot):
    await bot.add_cog(TeamCog(bot))