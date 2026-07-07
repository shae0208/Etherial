import os
import discord
from typing import Any, Dict, Optional

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

        return None

    @staticmethod
    async def add_submission(
        submission: Dict[str, Any],
        bot: Optional[discord.Client] = None,
        owner_id: Optional[int] = os.getenv("OWNER_USER_ID"),
    ) -> Dict[str, Any]:
        payload = {
            "animus": submission.get('animus', '').strip(),
            "path": submission.get('path', '').strip(),
            "value": submission.get('value', '').strip(),
            "reason": submission.get('reason', '').strip(),
            "submitted_by": submission.get('submitted_by', 'Unknown').strip() or 'Unknown',
            "is_premium": bool(submission.get('is_premium', False)),
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
                    
                    embed.add_field(name='Submitted by', value=payload.get('submitted_by'), inline=False)
                    embed.add_field(name='Premium', value=('Yes' if payload.get('is_premium') else 'No'), inline=False)
                    embed.add_field(name='Animus', value=payload.get('animus') or 'No value provided.', inline=False)
                    embed.add_field(name='Field', value=payload.get('path') or 'No value provided.', inline=False)
                    embed.add_field(name='Suggested value', value=payload.get('value') or 'No value provided.', inline=False)
                    
                    if payload['reason']:
                        embed.add_field(name='Reason', value=payload.get('reason'), inline=False)

                    await user.send(embed=embed)
                    
                    delivered = True
                    
            except Exception:
                delivered = False

        return {
            "status": "queued" if delivered else "queued_pending_dm",
            "submission": payload,
            "delivered": delivered,
        }
