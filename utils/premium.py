import os
from functools import wraps
from typing import Optional


def get_premium_sku_id() -> Optional[int]:
    value = os.getenv('DISCORD_PREMIUM_SKU_ID')
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

    entitlement_sku_ids = getattr(interaction, 'entitlement_sku_ids', None) or []
    if target_sku_id in entitlement_sku_ids:
        return True

    guild = getattr(interaction, 'guild', None)
    if guild is not None:
        guild_entitlement_sku_ids = getattr(guild, 'entitlement_sku_ids', None) or []
        if target_sku_id in guild_entitlement_sku_ids:
            return True

    return False


def require_premium(sku_id: Optional[int] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction, *args, **kwargs):
            if not has_premium_access(interaction, sku_id):
                await interaction.response.send_message(
                    "This command requires an active premium entitlement for this app.",
                    ephemeral=True,
                )
                return
            return await func(self, interaction, *args, **kwargs)

        return wrapper

    return decorator
