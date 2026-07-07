import discord
from discord.ext import commands
from discord import app_commands
from services.animus_service import AnimusService

class AnimusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='animus', description='View currently supported animus.')
    async def animus(self, interaction: discord.Interaction):
        data = AnimusService.get_supported_animus()
        
        ssr_names = data.get('SSR', [])
        sr_names = data.get('SR', [])
        r_names = data.get('R', [])

        if not ssr_names and not sr_names and not r_names:
            await interaction.response.send_message('No supported animus found.', ephemeral=True)
            return

        embed = discord.Embed(
            title='Supported Animus',
            description='Current roster supported by Etherial.',
            color=discord.Color.blurple()
        )
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        embed.add_field(
            name = 'SSR',
            value = '\n'.join(ssr_names) or 'No SSR animus found.',
            inline = True
        )
        embed.add_field(
            name = 'SR',
            value = '\n'.join(sr_names) or 'No SR animus found.',
            inline = True
        )
        embed.add_field(
            name = 'R',
            value = '\n'.join(r_names) or 'No R animus found.',
            inline = True
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AnimusCog(bot))