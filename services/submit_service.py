import os
from typing import Any, Dict, Optional

import discord


class SubmitService:
    @staticmethod
    def resolve_owner_id(bot: Optional[discord.Client] = None, owner_id: Optional[int] = None) -> Optional[int]:
        if owner_id is not None:
            return int(owner_id)

        if bot is not None:
            if getattr(bot, "owner_id", None):
                return int(bot.owner_id)

            application = getattr(bot, "application", None)
            owner = getattr(application, "owner", None)
            
            if owner is not None:
                return int(owner.id)

        env_id = os.getenv("OWNER_DISCORD_ID") or os.getenv("OWNER_USER_ID")
        
        if env_id:
            try:
                return int(env_id)
            except ValueError:
                return None

        return None

    @staticmethod
    async def add_submission(
        submission: Dict[str, Any],
        bot: Optional[discord.Client] = None,
        owner_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload = {
            "animus": submission.get("animus", "").strip(),
            "path": submission.get("path", "").strip(),
            "value": submission.get("value", "").strip(),
            "reason": submission.get("reason", "").strip(),
            "submitted_by": submission.get("submitted_by", "Unknown").strip() or "Unknown",
        }

        target_id = SubmitService.resolve_owner_id(bot=bot, owner_id=owner_id)
        delivered = False

        if target_id is not None and bot is not None:
            try:
                user = bot.get_user(target_id)
                
                if user is None:
                    user = await bot.fetch_user(target_id)

                if user is not None:
                    embed = discord.Embed(
                        title="New Animus Suggestion",
                        description="A new suggestion form submission was received.",
                        color=discord.Color.blurple(),
                    )
                    
                    embed.add_field(name="Submitted by", value=payload["submitted_by"], inline=False)
                    embed.add_field(name="Animus", value=payload["animus"] or "Unknown", inline=False)
                    embed.add_field(name="Field", value=payload["path"] or "Unknown", inline=False)
                    embed.add_field(name="Suggested value", value=payload["value"] or "No value provided", inline=False)
                    
                    if payload["reason"]:
                        embed.add_field(name="Reason", value=payload["reason"], inline=False)

                    await user.send(embed=embed)
                    
                    delivered = True
                    
            except Exception:
                delivered = False

        return {
            "status": "queued" if delivered else "queued_pending_dm",
            "submission": payload,
            "delivered": delivered,
        }
