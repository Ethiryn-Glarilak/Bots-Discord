import discord
import dotenv
import os
import src

from discord.ext import commands
from extensions.EPTV.schema import Base, EventEPTVPresence

class EPTV(commands.Cog):
    """EPTV extension for the bot."""

    EPTV_GUILD_ID = int(os.getenv("EPTV_GUILD_ID","0"))

    def __init__(self, bot: src.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log(name="EPTV").info("EPTV extension is ready.")
        self.bot.database().create_schema("eptv", Base)

    @discord.app_commands.command(
        name="eptv_presence",
        description="Permet d'indiquer votre présence à un événement EPTV."
    )
    @discord.app_commands.describe(
        name="Nom de l'évènement",
        content="Remarque concernant votre présence"
    )
    # @discord.app_commands.guilds(discord.Object(self.EPTV_GUILD_ID))  # EPTV Server ID
    async def command_presence_information(self, ctx: discord.Interaction, name: str, content: str):
        """Indicate your presence at an EPTV event."""
        self.bot.log(name="EPTV").info(f"Presence command invoked by {ctx.user.name} for event '{name}' with content: {content}")
        
        guild_eptv = self.bot.get_guild(self.EPTV_GUILD_ID)
        if not guild_eptv:
            await ctx.response.send_message("EPTV guild not found.", ephemeral=True)
            return

        guild_events = guild_eptv.scheduled_events
        event = None
        for guild_event in guild_events:
            if guild_event.name == name:
                event = guild_event
                break
        if not event:
            await ctx.response.send_message(f"No event found with the name '{name}'.", ephemeral=True)
            return

        # Attention si le user à déjà répondu on doit écraser la réponse
        existing_presence = self.bot.database().get_filtered(EventEPTVPresence, event_id=event.id, user_id=ctx.user.id)
        if existing_presence:
            existing_presence = existing_presence[0]  # Get the first presence if multiple exist
            existing_presence.content = content
            self.bot.database().update(existing_presence)
        else:
            presence = EventEPTVPresence(event_id=event.id, user_id=ctx.user.id, content=content)
            self.bot.database().add(presence)

        if not event.description:
            event.description = "### Présences ###\n"
        else:
            if "### Présences ###" in event.description:
                event.description = event.description.split("### Présences ###")[0].strip()
                event.description += "\n### Présences ###\n"
            else:
                event.description += "\n### Présences ###\n"

        presence_list = self.bot.database().get_filtered(EventEPTVPresence, event_id=event.id)
        if not presence_list:
            await ctx.response.send_message("No presence information found for this event.", ephemeral=True)
            return

        presence_info = ""
        for presence in presence_list:
            user = self.bot.get_user(presence.user_id)
            if user:
                presence_info += f"{user.display_name} - {presence.content}\n"
            else:
                presence_info += f"Unknown User (ID: {presence.user_id}) - {presence.content}\n"        

        event.description += f"\n{presence_info}"
        await event.edit(description=event.description)
        self.bot.log(name="EPTV").info(f"Presence information for '{name}' updated with note: {content}")

        await ctx.response.send_message(f"Your presence for '{name}' has been recorded with note: {content}", ephemeral=True)

    def get_list_of_events(self):
        """Retrieve the list of EPTV events from the database."""
        guild_eptv = self.bot.get_guild(self.EPTV_GUILD_ID)  # EPTV Server ID
        if not guild_eptv:
            self.bot.log(name="EPTV").error("EPTV guild not found.")
            return []
        return guild_eptv.scheduled_events

    @command_presence_information.autocomplete("name")
    async def choice_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplete for the event name choice."""
        # Assuming get_list_of_events is a method that retrieves events from the database
        return [discord.app_commands.Choice(name=event.name, value=event.name) for event in self.get_list_of_events() if current.lower() in event.name.lower()]

async def setup(bot: src.Bot):
    """Setup function to add the EPTV cog to the bot."""
    bot.log(name="EPTV").info("Loading EPTV extension...")
    dotenv.load_dotenv()
    await bot.add_cog(EPTV(bot))
