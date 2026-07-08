import discord
from discord.ext import commands
from discord import app_commands
from services.counter_service import CounterService
from utils.premium import require_premium


class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='counter', description='View counter recommendations for the selected animus.')
    @require_premium()
    async def counter(self, interaction: discord.Interaction, animus: str):
        data = CounterService.get_counters(animus)

        if not data:
            await interaction.response.send_message("Animus not found.", ephemeral=True)
            return

        image_url = data.get('image')
        color_data = data.get('element')
        
        color_map = {
            'Red': discord.Color.red(),
            'Blue': discord.Color.blue(),
            'Green': discord.Color.green(),
            'Light': discord.Color.gold(),
            'Dark': discord.Color.purple()
        }
        
        embed = discord.Embed(title=f"{data.get('name')} Counter Analysis", color=color_map.get(color_data))
        
        if image_url:
            embed.set_thumbnail(url=image_url or self.bot.user.display_avatar.url)
                        
        embed.add_field(
            name = "Countered By:",
            value = '\n'.join(data.get('countered_by', [])) or 'No counter recommendations available.',
            inline = False
        )
        embed.add_field(
            name = "Counters:",
            value = '\n'.join(data.get('counters', [])) or 'No counter recommendations available.',
            inline = False,
        )

        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(CounterCog(bot))