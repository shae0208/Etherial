import discord
from discord.ext import commands
from discord import app_commands
from services.counter_service import CounterService


class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='counter', description='Show counters for an Animus.')
    async def counter(self, interaction: discord.Interaction, animus: str):
        counters = CounterService.get_counters(animus)

        if not counters:
            await interaction.response.send_message(
                "Animus not found."
            )
            return

        embed = discord.Embed(title=f"{counters['name']} Counters")
        image_url = counters.get('image')
        
        if image_url:
            embed.set_thumbnail(url=image_url)
            
        embed.add_field(
            name = "Counters",
            value = '\n'.join(counters.get('counters', [])) or 'No counter data available.',
            inline = False,
        )

        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(CounterCog(bot))