import discord
from discord.ext import commands
import random

class Facts(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    # --- Example dataset ---
    facts = [
        "The first computer virus was created in 1986 and was called Brain.",
        "Phishing accounts for over 90% of all data breaches.",
        "Cybersecurity spending exceeded $200 billion globally in 2024.",
        "The word 'hacker' originally meant a skilled programmer, not a criminal."
    ]

    @commands.command(name="fact")
    async def cyberfact(self, ctx):
        fact = random.choice(self.facts)
        await ctx.send(f"💡 {fact}")


async def setup(bot):
    await bot.add_cog(Facts(bot))
