import discord
from discord.ext import commands
import random

# --- Bot setup ---
intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages

bot = commands.Bot(command_prefix="/", intents=intents)

# --- Example dataset ---
facts = [
        "The first computer virus was created in 1986 and was called Brain.",
    "Phishing accounts for over 90% of all data breaches.",
    "Cybersecurity spending exceeded $200 billion globally in 2024.",
    "The word 'hacker' originally meant a skilled programmer, not a criminal."
]

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")

@bot.command()
async def cyberfact(ctx):
    fact = random.choice(facts)
    await ctx.send(f"💡 {fact}")

bot.run("MTQzMzU4MDQxODM3MTk0ODU2NA.GLi7XP.uCETfKJfT1huZ6V6oTUjRKpe_GQFjjeT42UwFc")
