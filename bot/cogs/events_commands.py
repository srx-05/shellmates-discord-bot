import discord
from discord.ext import commands
from datetime import datetime
from database.Repositories.eventRepo import EventRepository

ALLOWED_ROLES = ["Mod", "Admin"]


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = EventRepository()

    # ------------------------------------------------------------
    # Helper: Check if user has allowed role
    # ------------------------------------------------------------
    def has_allowed_role(self, user_roles):
        allowed_lower = [role.lower() for role in ALLOWED_ROLES]
        return any(role.name.lower() in allowed_lower for role in user_roles)

    # ------------------------------------------------------------
    # !add_event <title> <date> <description>
    # ------------------------------------------------------------
    @commands.command(name="add_event", help="Add a new event (Admin/Mod only).")
    async def add_event(self, ctx, title: str, date: str, *, description: str):
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission to add events.")
            return

        try:
            # Parse the date string to datetime
            event_date = datetime.fromisoformat(date)

            # Check for duplicates
            existing_events = self.repo.get_upcoming_events()
            for event in existing_events:
                if event[1].lower() == title.lower() and event[3].strftime(
                    "%Y-%m-%d %H:%M"
                ) == event_date.strftime("%Y-%m-%d %H:%M"):
                    await ctx.send(
                        f"⚠️ An event titled **{title}** already exists at that date/time."
                    )
                    return

            # Create event
            event = self.repo.create_event(
                title=title,
                description=description,
                event_date=event_date,
                created_by=str(ctx.author.id),
                channel_id=str(ctx.channel.id),
                message_id=None,
            )

            await ctx.send(
                f"✅ New event **{event[1]}** scheduled for `{event_date.strftime('%Y-%m-%d %H:%M')}`!"
            )

        except ValueError:
            await ctx.send(
                "⚠️ Invalid date format! Use `YYYY-MM-DDTHH:MM` (ISO format)."
            )
        except Exception as e:
            await ctx.send(f"❌ Failed to create event: {e}")

    # ------------------------------------------------------------
    # !remove_event <event_id or title>
    # ------------------------------------------------------------
    @commands.command(name="remove_event", help="Remove an event by ID or title.")
    async def remove_event(self, ctx, *, identifier: str):
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission to remove events.")
            return

        deleted = False

        # Try to interpret as numeric ID
        if identifier.isdigit():
            self.repo.delete_event(int(identifier))
            deleted = True
        else:
            # Try deleting by title
            events = self.repo.get_upcoming_events()
            for event in events:
                if event[1].lower() == identifier.lower():
                    self.repo.delete_event(event[0])
                    deleted = True
                    break

        if deleted:
            await ctx.send(f"🗑️ Event `{identifier}` has been removed.")
        else:
            await ctx.send(f"⚠️ No event found with ID or title `{identifier}`.")

    # ------------------------------------------------------------
    # !events → List upcoming events
    # ------------------------------------------------------------
    @commands.command(name="events", help="List all upcoming events.")
    async def list_events(self, ctx):
        events = self.repo.get_upcoming_events()

        if not events:
            await ctx.send("📭 No upcoming events found.")
            return

        embed = discord.Embed(
            title="📅 Upcoming Events",
            color=discord.Color.green(),
            timestamp=datetime.now(),
        )

        for e in events:
            event_id, title, desc, date, created_by, _, _, _ = e
            embed.add_field(
                name=f"#{event_id} — {title}",
                value=f"📆 `{date.strftime('%Y-%m-%d %H:%M')}`\n📝 {desc[:150]}...",
                inline=False,
            )

        await ctx.send(embed=embed)

    # ------------------------------------------------------------
    # !past_events → List past events
    # ------------------------------------------------------------
    @commands.command(name="past_events", help="Show past events.")
    async def past_events(self, ctx):
        past = self.repo.get_past_events()

        if not past:
            await ctx.send("🕰️ No past events yet.")
            return

        embed = discord.Embed(
            title="📜 Past Events",
            color=discord.Color.orange(),
            timestamp=datetime.now(),
        )

        for e in past:
            event_id, title, desc, date, created_by, _, _, _ = e
            embed.add_field(
                name=f"#{event_id} — {title}",
                value=f"📆 `{date.strftime('%Y-%m-%d %H:%M')}`\n📝 {desc[:150]}...",
                inline=False,
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Events(bot))
