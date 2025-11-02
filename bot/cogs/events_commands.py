import discord
from discord.ext import commands
import random

class Events(commands.Cog): 
      def __init__(self, bot):
        self.bot = bot





########### EVENTS COMMAND LOGIC SHOULD BE INSIDE THIS CLASS













async def setup(bot):
    await bot.add_cog(Events(bot))