import discord
from discord.ext import commands
import random

class Events(commands.Cog): 
      def __init__(self, bot):
        self.bot = bot






@commands.command(name="add_event")
@commands.has_permissions(administrator=True)
async def add_event(ctx, title: str, date: str, description: str, location: str):
    em.add_event(title, date, description, location)
    await ctx.send(f"new event {title}")

@commands.command(name="remove_event")
@commands.has_permissions(administrator=True)
async def remove_event(ctx, *, title: str):
    deleted = em.remove_event(title)
    if deleted:
        await ctx.send(f"{title} removed")
    else:
        await ctx.send(f"this event doesent existe {title}")










async def setup(bot):
    await bot.add_cog(Events(bot))