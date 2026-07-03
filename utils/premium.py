import os
import discord
from functools import wraps
from typing import Optional

class PremiumView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        sku_id = os.getenv('PREMIUM_SKU_ID')

        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.premium,
                sku_id=sku_id,
            )
        )

def get_premium_sku_id() -> Optional[int]:
    value = os.getenv('PREMIUM_SKU_ID')
    
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None

def has_premium_access(interaction, sku_id: Optional[int] = None) -> bool:
    target_sku_id = sku_id or get_premium_sku_id()
    
    if target_sku_id is None:
        return False

    entitlements = getattr(interaction, "entitlements", [])
        
    for entitlement in entitlements: 
        if entitlement.sku_id == target_sku_id:
            return True
    
    return False

def require_premium(sku_id: Optional[int] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction, *args, **kwargs):
            if not has_premium_access(interaction, sku_id):
                embed = discord.Embed(
                    title = '🔒 Premium Feature',
                    description = (
                        "This command requires Etherial Premium.\n\n"
                        "Purchase below to unlock advanced PvP tools:\n"
                        " `/teams`\n"
                        " `/counters`\n"
                        " `/speedtune`\n"
                        " `/draft`"
                    )
                )
                
                await interaction.response.send_message(
                    embed = embed,
                    view = PremiumView(),
                    ephemeral = True,
                )
                return
            
            return await func(self, interaction, *args, **kwargs)

        return wrapper

    return decorator
