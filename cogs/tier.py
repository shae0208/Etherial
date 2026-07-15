import discord
from discord.ext import commands
from discord import app_commands
from services.tier_service import TierService

class TierCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='tier', description='View current tier list.')
    async def animus(self, interaction: discord.Interaction):
        data = TierService.get_tierlist()
        
        t0_names = data.get('T0', [])
        t05_names = data.get('T0.5', [])
        t1_names = data.get('T1', [])
        t2_names = data.get('T2', [])
        t3_names = data.get('T3', [])
        t4_names = data.get('T4', [])
        t5_names = data.get('T5', [])

        if not t0_names and not t05_names and not t1_names and not t2_names and not t3_names and not t4_names and not t5_names:
            await interaction.response.send_message('No supported animus found.', ephemeral=True)
            return

        embed = discord.Embed(
            title='Tier List',
            description='Current PvP tier rankings',
            color=discord.Color.blurple()
        )
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        embed.add_field(
            name = 'Tier 0',
            value = '\n'.join(t0_names) or 'No animus found.',
            inline = True
        )
        embed.add_field(
            name = 'Tier 0.5',
            value = '\n'.join(t05_names) or 'No animus found.',
            inline = True
        )
        embed.add_field(
            name = 'Tier 1',
            value = '\n'.join(t1_names) or 'No animus found.',
            inline = True
        )
        embed.add_field(
            name = 'Tier 2',
            value = '\n'.join(t2_names) or 'No animus found.',
            inline = True
        )
        embed.add_field(
            name = 'Tier 3',
            value = '\n'.join(t3_names) or 'No animus found.',
            inline = True
        )
        embed.add_field(
            name = 'Tier 4',
            value = '\n'.join(t4_names) or 'No animus found.',
            inline = True
        )
        embed.add_field(
            name = 'Tier 5',
            value = '\n'.join(t5_names) or 'No animus found.',
            inline = True
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(TierCog(bot))