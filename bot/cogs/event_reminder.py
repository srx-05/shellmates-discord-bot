import discord
from discord.ext import commands, tasks
from datetime import datetime
from database.Repositories.EventReminderRepo import ReminderRepository

ALLOWED_ROLES = ["Mod", "Admin"]


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()
        self.cleanup_reminders.start()

    def has_allowed_role(self, user_roles):
        """Check if user has Mod or Admin role"""
        allowed_lower = [role.lower() for role in ALLOWED_ROLES]
        return any(role.name.lower() in allowed_lower for role in user_roles)

    # ----------------------------------------------------------------------
    @tasks.loop(seconds=60)
    async def check_reminders(self):
        """Check for upcoming events and send reminders via DM."""
        try:
            reminders = ReminderRepository.get_pending_reminders()
            print(f"🔔 Checking reminders... Found {len(reminders)} pending")

            for reminder in reminders:
                reminder_id, event_id, title, event_date, user_id, remind_before = (
                    reminder
                )

                try:
                    user = await self.bot.fetch_user(int(user_id))
                    if user:
                        event_time = (
                            event_date.strftime("%Y-%m-%d %H:%M")
                            if isinstance(event_date, datetime)
                            else str(event_date)
                        )

                        embed = discord.Embed(
                            title="⏰ Event Reminder!",
                            description=f"**{title}** starts in **{remind_before} minutes!**",
                            color=discord.Color.blue(),
                        )
                        embed.add_field(
                            name="📅 Start Time", value=event_time, inline=True
                        )
                        embed.add_field(
                            name="⏱️ Reminder Set",
                            value=f"{remind_before} minutes before",
                            inline=True,
                        )

                        await user.send(embed=embed)
                        print(f"✅ DM reminder sent to {user.name} for '{title}'")

                    ReminderRepository.mark_as_sent(reminder_id)

                except discord.Forbidden:
                    print(f"❌ Cannot send DM to user {user_id} (DMs closed)")
                except Exception as e:
                    print(f"⚠️ Failed to send reminder to {user_id}: {e}")

        except Exception as e:
            print(f"⚠️ Reminder check failed: {e}")

    # ----------------------------------------------------------------------
    @tasks.loop(hours=1)
    async def cleanup_reminders(self):
        """Clean up reminders for past events."""
        try:
            cleaned_count = ReminderRepository.cleanup_expired_reminders()
            if cleaned_count > 0:
                print(f"🧹 Cleaned up {cleaned_count} expired reminders")
        except Exception as e:
            print(f"⚠️ Cleanup failed: {e}")

    # ----------------------------------------------------------------------
    @commands.command(name="my_reminders", help="View your active reminders")
    async def my_reminders(self, ctx):
        """Show all your active reminders."""
        reminders = ReminderRepository.get_user_reminders(str(ctx.author.id))

        if not reminders:
            await ctx.send("📭 You have no active reminders.")
            return

        embed = discord.Embed(
            title="📋 Your Active Reminders", color=discord.Color.green()
        )

        for reminder in reminders:
            reminder_id, title, event_date, remind_before, sent, is_past = reminder
            event_time = event_date.strftime("%Y-%m-%d %H:%M")

            # Determine status based on both sent flag and whether event is past
            if sent:
                status = "✅ Sent"
            elif is_past:
                status = "❌ Missed (Event passed)"
            else:
                status = "⏰ Pending"

            embed.add_field(
                name=f"📌 {title}",
                value=f"**When:** {event_time}\n**Reminder:** {remind_before} min before\n**Status:** {status}",
                inline=False,
            )

        await ctx.send(embed=embed)

    # ----------------------------------------------------------------------
    @commands.command(
        name="cleanup_reminders",
        help="Manually clean up expired reminders (Mod/Admin only)",
    )
    async def cleanup_reminders_cmd(self, ctx):
        """Manually clean up expired reminders."""
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission.")
            return

        try:
            cleaned_count = ReminderRepository.cleanup_expired_reminders()
            await ctx.send(f"✅ Cleaned up {cleaned_count} expired reminders.")
        except Exception as e:
            await ctx.send(f"❌ Error cleaning reminders: {e}")

    # ----------------------------------------------------------------------
    @commands.command(
        name="remind_me", help="Subscribe to reminders for a specific event"
    )
    async def remind_me(self, ctx, event_id: int, remind_before: int = 60):
        """Subscribe to reminders for a specific event."""
        try:
            ReminderRepository.add_reminder_for_event(
                event_id=event_id,
                user_id=str(ctx.author.id),
                remind_before=remind_before,
            )

            await ctx.send(
                f"✅ You will receive a DM {remind_before} minutes before the event!"
            )

        except Exception as e:
            await ctx.send(f"❌ Error setting reminder: {e}")

    # ----------------------------------------------------------------------
    @commands.command(name="reminder_status", help="Check reminder service status")
    async def reminder_status(self, ctx):
        """Check if reminder service is running."""
        status = "🟢 RUNNING" if self.check_reminders.is_running() else "🔴 STOPPED"
        embed = discord.Embed(
            title="Reminder Service Status",
            description=f"Current status: **{status}**",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    # ----------------------------------------------------------------------
    @commands.command(
        name="start_reminders", help="Start automatic event reminders (Mod/Admin only)"
    )
    async def start_reminders(self, ctx):
        """Start automatic event reminders."""
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission to start reminders.")
            return

        if not self.check_reminders.is_running():
            self.check_reminders.start()
            await ctx.send("✅ Event reminders started!")
        else:
            await ctx.send("⚠️ Reminder service is already running.")

    # ----------------------------------------------------------------------
    @commands.command(
        name="stop_reminders", help="Stop automatic event reminders (Mod/Admin only)"
    )
    async def stop_reminders(self, ctx):
        """Stop automatic event reminders."""
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission to stop reminders.")
            return

        if self.check_reminders.is_running():
            self.check_reminders.cancel()
            await ctx.send("🛑 Event reminders stopped.")
        else:
            await ctx.send("⚠️ Reminder service is not running.")

    # ----------------------------------------------------------------------


async def setup(bot):
    await bot.add_cog(ReminderCog(bot))
