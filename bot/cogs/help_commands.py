import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Temporary command list
        self.commands_data = [
            {
                "name": "fact",
                "description": "Sends a random cybersecurity fact.",
                "usage": "/fact",
            },
            {
                "name": "event",
                "description": "Displays upcoming club events.",
                "usage": "/event",
            },
            {
                "name": "quiz",
                "description": "Starts a cybersecurity quiz based on posted facts.",
                "usage": "/quiz",
            },
            {
                "name": "help",
                "description": "Shows a list of all available commands.",
                "usage": "/help [command]",
            }
        ]

    @commands.command(name="help")
    async def help(self, ctx, command_name: str = ""):
        # If user requests help for a specific command
        if command_name:
            command = next((cmd for cmd in self.commands_data if cmd["name"] == command_name), None)
            if command:
                embed = discord.Embed(
                    title=f"📘 Help: `{command['name']}`",
                    description=command["description"],
                    color=discord.Color.blue()
                )
                embed.add_field(name="Usage", value=f"`{command['usage']}`", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ No command called `{command_name}` found.", ephemeral=True)
            return

        # General help embed
        embed = discord.Embed(
            title="🤖 Shellmates Bot Commands",
            description="Here’s a list of all available commands:",
            color=discord.Color.blurple()
        )

        commands_description = "\n".join(
            [f"`{cmd['usage']}` — {cmd['description']}" for cmd in self.commands_data]
        )

        embed.add_field(name="Commands", value=commands_description, inline=False)
        embed.set_footer(text="Use /help <command> for more details about a specific command.")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
