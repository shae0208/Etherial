import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='help', description='View useful information about the bot.')
    async def help(self, interaction: discord.Interaction):
        overview = (
            "Etherial is a competitive PvP utility bot for Etheria Restart,"
            " created to help players master the arena through optimized"
            " builds, matchup analysis, counter recommendations, and meta-"
            "focused insights.\n\n" 
            "Built for serious competitors and unions looking to gain every possible advantage!"
        )
        
        commands = (
            "/help - View Etherial support information.\n"
            "/build - View build guide for the selected animus.\n"
            "/team - View team recommendations for the selected animus.\n"
            "/counter - View counter recommendations for the selected animus.\n"
            "/compare - View comparison of two selected animus.\n"
            "/speedtune - View speed tuning recommendations for selected team.\n"
            "/draft - View ban recommendations for selected enemy draft.\n"
            "/submit - Suggest a change to animus data for review."
        )

        contact = (
            "Please contact bl4ckh4wkttv.gaming@gmail.com for additional support.\n\n"
            "Feel free to also provide suggestions/feedback about the bot in general,"
            " or to suggest edits to inaccurate information to better the experience."
        )
        
        embed = discord.Embed(title='Etherial Support', description=overview)
        
        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(name='Commands', value=commands, inline=False)
        embed.add_field(name='Contact', value=contact, inline=False)
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(HelpCog(bot))