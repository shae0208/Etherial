import discord
from discord.ext import commands
from discord import app_commands
from services.animus_service import AnimusService


class AnimusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='animus', description='View all supported animus by rarity.')
    async def animus(self, interaction: discord.Interaction):
        supported = AnimusService.get_supported_animus()
        ssr_names = supported.get('SSR', [])
        sr_names = supported.get('SR', [])
        r_names = supported.get('R', [])

        if not ssr_names and not sr_names and not r_names:
            await interaction.response.send_message('No supported animus found.', ephemeral=True)
            return

        embed = discord.Embed(
            title='Supported Animus',
            description='Current roster supported by Etherial.'
        )
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        embed.add_field(name='SSR', value='\n'.join(ssr_names) or 'None', inline=True)
        embed.add_field(name='SR', value='\n'.join(sr_names) or 'None', inline=True)
        embed.add_field(name='R', value='\n'.join(r_names) or 'None', inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(AnimusCog(bot))