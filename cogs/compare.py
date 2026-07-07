import discord
from discord.ext import commands
from discord import app_commands
from services.compare_service import CompareService

class CompareCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='compare', description='View comparison of the selected animus.')
    async def compare(self, interaction: discord.Interaction, animus1: str, animus2: str):
        data = CompareService.get_comparison_data(animus1, animus2)
        
        if not data:
            await interaction.response.send_message("One or both Animus not found.", ephemeral=True)
            return
        
        unit1 = data.get('animus1')
        unit2 = data.get('animus2')
        
        def format_unit(unit):
            return (
                f"Role: {unit.get('role')}\n"
                f"Element: {unit.get('element')}\n"
                f"Speed: {unit.get('base_speed')}\n"
                f"Lattice: {unit.get('lattice')}"
            )
            
        embed = discord.Embed(title=f"{unit1.get('name')} vs {unit2.get('name')}", color=discord.Color.blurple())
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        embed.add_field(
            name = unit1.get('name'),
            value = f"{format_unit(unit1)}",
            inline = True
        )
        embed.add_field(
            name = unit2.get('name'),
            value = f"{format_unit(unit2)}",
            inline = True
        )
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(CompareCog(bot))