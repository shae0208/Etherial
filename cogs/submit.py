import discord
from discord.ext import commands
from discord import app_commands

from services.submit_service import SubmitService


class SubmitModal(discord.ui.Modal, title="Suggest an update to animus information"):
    animus = discord.ui.TextInput(
        label="Animus Name",
        placeholder="Enter the animus name",
        required=True,
        max_length=80,
    )
    field = discord.ui.TextInput(
        label="Field to Update",
        placeholder="Example: build.shells or role",
        required=True,
        max_length=120,
    )
    value = discord.ui.TextInput(
        label="Suggested Value",
        placeholder="Enter the replacement value",
        required=True,
        max_length=500,
    )
    reason = discord.ui.TextInput(
        label="Why this should change",
        placeholder="Brief explanation",
        required=False,
        max_length=500,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        submission = {
            "animus": self.animus.value,
            "path": self.field.value,
            "value": self.value.value,
            "reason": self.reason.value,
            "submitted_by": str(interaction.user),
        }

        result = await SubmitService.add_submission(submission, bot=self.bot)
        
        if result.get("delivered"):
            await interaction.response.send_message(
                "Your suggestion has been sent directly to the owner for review. Thanks for helping improve the data!",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Your suggestion was received, but I could not reach the owner through Discord DMs right now. Please try again later.",
                ephemeral=True,
            )


class SubmitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="submit", description="Submit a suggested change to animus data.")
    async def submit(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SubmitModal(self.bot))


async def setup(bot):
    await bot.add_cog(SubmitCog(bot))
