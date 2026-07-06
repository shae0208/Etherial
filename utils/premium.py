import os
import discord
from functools import wraps
from typing import Optional


class PremiumView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for sku_id in get_premium_sku_ids():
            self.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.premium,
                    sku_id=sku_id,
                )
            )

def _parse_sku_ids(value: Optional[str]) -> list[int]:
    if not value:
        return []

    sku_ids = []
    
    for part in value.replace(';', ',').split(','):
        cleaned = part.strip()
        if not cleaned:
            continue
        try:
            sku_ids.append(int(cleaned))
        except ValueError:
            continue

    return sku_ids

def get_premium_sku_ids() -> list[int]:
    discovered_ids = []
    for env_name in ('PREMIUM_SKU_ID', 'PREMIUM_SKU_ID_2', 'PREMIUM_SKU_IDS'):
        discovered_ids.extend(_parse_sku_ids(os.getenv(env_name)))

    unique_ids = []
    seen_ids = set()
    
    for sku_id in discovered_ids:
        if sku_id not in seen_ids:
            unique_ids.append(sku_id)
            seen_ids.add(sku_id)

    return unique_ids

def get_premium_sku_id() -> Optional[int]:
    sku_ids = get_premium_sku_ids()
    return sku_ids[0] if sku_ids else None

def has_premium_access(interaction, sku_id: Optional[int] = None) -> bool:
    if sku_id is None:
        target_sku_ids = get_premium_sku_ids()
    else:
        target_sku_ids = [sku_id]

    if not target_sku_ids:
        return False

    entitlements = getattr(interaction, "entitlements", []) or []
    guild_id = getattr(interaction, "guild_id", None)
    user = getattr(interaction, "user", None)
    user_id = getattr(user, "id", None)

    for entitlement in entitlements:
        if getattr(entitlement, "deleted", False):
            continue

        if getattr(entitlement, "sku_id", None) not in target_sku_ids:
            continue

        if getattr(entitlement, "is_expired", lambda: False)():
            continue

        entitlement_guild_id = getattr(entitlement, "guild_id", None)
        entitlement_user_id = getattr(entitlement, "user_id", None)

        if entitlement_guild_id is not None and guild_id is not None and entitlement_guild_id == guild_id:
            return True

        if entitlement_user_id is not None and user_id is not None and entitlement_user_id == user_id:
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
