import discord
from discord.ext import commands
from discord import app_commands
from services.counter_service import CounterService
from utils.premium import require_premium


class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='counter', description='View counter recommendations for the selected animus.')
    # @require_premium()
    async def counter(self, interaction: discord.Interaction, animus: str):
        counters = CounterService.get_counters(animus)

        if not counters:
            await interaction.response.send_message(
                "Animus not found."
            )
            return

        embed = discord.Embed(title=f"{counters['name']} Counters")
        image_url = counters.get('image')
        color_data = counters.get('element')
        
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
            name = "Counters",
            value = '\n'.join(counters.get('counters', [])) or 'No counter data available.',
            inline = False,
        )

        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(CounterCog(bot))