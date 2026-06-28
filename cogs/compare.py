import discord
from discord.ext import commands
from discord import app_commands
from services.compare_service import CompareService

class CompareCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='compare', description='Compare Two Animus')
    async def compare(self, interaction: discord.Interaction, animus1: str, animus2: str):
        result = CompareService.compare(animus1, animus2)
        
        if not result:
            await interaction.response.send_message(
                "One or both Animus not found."
            )
            return
        
        unit1 = result["animus1"]
        unit2 = result["animus2"]
        
        embed = discord.Embed(title=f"{unit1['name']} vs {unit2['name']}")
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        embed.add_field(
            name = unit1['name'],
            value = 
                f'Role: {unit1['role']}\n'
                f'Element: {unit1['element']}\n'
                f'Speed: {unit1['base_speed']}\n'
                f'Lattice: {unit1['lattice']}',
                inline = True
        )
        embed.add_field(
            name = unit2['name'],
            value = 
            f'Role: {unit2['role']}\n'
            f'Element: {unit2['element']}\n'
            f'Speed: {unit2['base_speed']}\n'
            f'Lattice: {unit2['lattice']}',
            inline = True
        )
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(CompareCog(bot))