import discord
import os

class PremiumView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        id = os.getenv('PREMIUM_SKU_ID')
        
        self.add_item(
            discord.ui.Button(
                style = discord.ButtonStyle.premium,
                sku_id = id
            )
        )