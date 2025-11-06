import discord
from discord.ext import commands, tasks
from datetime import datetime
from database.reminder_repo import ReminderRepository


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        ReminderRepository.create_table()
        self.check_reminders.start()

    # ----------------------------------------------------------------------
    @tasks.loop(seconds=60)
    async def check_reminders(self):
        """Check for upcoming events and send reminders."""
        try:
            reminders = ReminderRepository.get_pending_reminders()
            for reminder in reminders:
                reminder_id, event_id, title, event_date, channel_id, remind_before = (
                    reminder
                )

                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    embed = discord.Embed(
                        title="⏰ Upcoming Event Reminder!",
                        description=f"**{title}** starts in **{remind_before} minutes!**\n📅 **Start time:** {event_date}",
                        color=discord.Color.green(),
                    )
                    await channel.send(embed=embed)
                    print(f"✅ Reminder sent for '{title}'.")

                ReminderRepository.mark_as_sent(reminder_id)

        except Exception as e:
            print(f"⚠️ Reminder check failed: {e}")

    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_event_created(self, event_id):
        """When a new event is created, add a reminder automatically."""
        ReminderRepository.add_reminder_for_event(event_id)
        print(f"🗓️ Added reminder for event ID {event_id}.")

    # ----------------------------------------------------------------------
    @commands.command(name="start_reminders")
    async def start_reminders(self, ctx):
        """Start automatic event reminders."""
        if not self.check_reminders.is_running():
            self.check_reminders.start()
            await ctx.send("✅ Event reminders started!")
        else:
            await ctx.send("⚠️ Reminder service is already running.")

    @commands.command(name="stop_reminders")
    async def stop_reminders(self, ctx):
        """Stop automatic event reminders."""
        if self.check_reminders.is_running():
            self.check_reminders.cancel()
            await ctx.send("🛑 Event reminders stopped.")
        else:
            await ctx.send("⚠️ Reminder service is not running.")


async def setup(bot):
    await bot.add_cog(ReminderCog(bot))
