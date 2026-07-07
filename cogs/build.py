import discord
from discord.ext import commands
from discord import app_commands
from services.build_service import BuildService

class BuildCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='build', description='View PvP build recommendations for the selected animus.')
    async def build(self, interaction: discord.Interaction, animus: str):
        build = BuildService.get_build(animus)
        
        if not build:
            await interaction.response.send_message("Animus not found.", ephemeral = True)
            return

        build_data = build.get('build')
        image_url = build.get('image')
        color_data = build.get('element')
        
        color_map = {
            'Red': discord.Color.red(),
            'Blue': discord.Color.blue(),
            'Green': discord.Color.green(),
            'Light': discord.Color.gold(),
            'Dark': discord.Color.purple()
        }
        
        embed = discord.Embed(title=f"{build.get('name')} PvP Build", color=color_map.get(color_data))
        
        if image_url:
            embed.set_thumbnail(url=image_url or self.bot.user.display_avatar.url)
                    
        embed.add_field(
            name = 'Lattice Requirements',
            value = build.get('lattice') or 'No lattice recommendations available',
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