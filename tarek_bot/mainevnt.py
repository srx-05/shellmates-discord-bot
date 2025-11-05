import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import event as em
def load_bad_words():
   
        with open("badwords.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
bad_words = load_bad_words()
load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
secret_role = "hh"


@bot.command(name="add_event")
@commands.has_permissions(administrator=True)
async def add_event(ctx, title: str, date: str, description: str, location: str):
    em.add_event(title, date, description, location)
    await ctx.send(f"new event {title}")

@bot.command(name="remove_event")
@commands.has_permissions(administrator=True)
async def remove_event(ctx, *, title: str):
    deleted = em.remove_event(title)
    if deleted:
        await ctx.send(f"{title} removed")
    else:
        await ctx.send(f"this event doesent existe {title}")

@bot.command(name="events")
async def events(ctx):
    events_text = em.list_events()
    await ctx.send(events_text)



@bot.event
async def on_ready():
    print(f" we are ready to go in , {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f" welcom to the serveur test ,{member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(bad_word in message.content.lower() for bad_word in bad_words):
        await message.delete()
        await message.channel.send(
            f"{message.author.mention}  dont use this word a admin will come to you"
        )

        admin_role = discord.utils.get(message.guild.roles, name=secret_role)
        if admin_role:
            for member in message.guild.members:
                if admin_role in member.roles:
                    try:
                        await member.send(
                            f" Alert the user  {message.author} said {message.content}in: #{message.channel.name}.\n> "
                        )
                    except:
                        pass

    await bot.process_commands(message)

   

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist.")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had   {secret_role}remove")
    else:
        await ctx.send("Role doesn't exist.")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"you said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("this is a reply to your message!")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("welcome to our club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"{ctx.author.mention} dont have the permision to do that !")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)




