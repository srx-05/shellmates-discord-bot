import discord
from discord.ext import commands
import random
from database.Repositories.eventRepo import EventRepository


ALLOWED_ROLES = ["Mod", "Admin"]


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = EventRepository()


def has_allowed_role(self, user_roles):

    allowed_lower = [role.lower() for role in ALLOWED_ROLES]
    return any(role.name.lower() in allowed_lower for role in user_roles)


@commands.command(name="add_event")
async def add_event(self, ctx, title: str, date: str, description: str, location: str):
    if not self.has_allowed_role(ctx.author.roles):
        await ctx.send("❌ You don't have permission to add commands.")
        return

    try:
        self.repo.create_event(title, date, description, location)
        await ctx.send(f"new event {title}")

    except Exception as e:
        await ctx.send(f"❌ Failed to add event: {e}")


@commands.command(name="remove_event")
@commands.has_permissions(administrator=True)
async def remove_event(self, ctx, *, title: str):
    deleted = self.repo.remove_event(title)
    if deleted:
        await ctx.send(f"{title} removed")
    else:
        await ctx.send(f"this event doesent existe {title}")


async def setup(bot):
    await bot.add_cog(Events(bot))
