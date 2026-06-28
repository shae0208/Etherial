import discord
from discord.ext import commands
from discord import app_commands
from services.build_service import BuildService

class BuildCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='build', description='View PvP build recommendations.')
    async def build(self, interaction: discord.Interaction, animus: str):
        build = BuildService.get_build(animus)
        
        if not build:
            await interaction.response.send_message(
                "Animus not found."
            )
            return

        embed = discord.Embed(title=f"{build['name']} PvP Build")
        build_data = build.get('build')
        image_url = build.get('image')
        lattice_data = build.get('lattice')
        color_data = build.get('element')
        
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
            
        embed.add_field(
            name = 'Lattice Requirements',
            value = lattice_data or 'No lattice requirements available',
            inline = False 
        )
        embed.add_field(
            name = 'Recommended Shells',
            value = '\n'.join(build_data.get('shells', [])) or 'No shell recommendations available.',
            inline = False
        )
        embed.add_field(
            name = 'Recommended Sets',
            value = '\n'.join(build_data.get('sets', [])) or 'No set recommendations available.',
            inline = False
        )
        embed.add_field(
            name = 'Main Stats',
            value = '\n'.join(build_data.get('mainstats', [])) or 'No mainstat recommendations available.',
            inline = False
        )
        embed.add_field(
            name = 'Substats',
            value = '\n'.join(build_data.get('substats', [])) or 'No substat recommendations available.',
            inline = False
        )
        
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(BuildCog(bot))