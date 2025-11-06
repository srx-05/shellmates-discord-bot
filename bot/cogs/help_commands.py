import discord
from discord.ext import commands
from database.Repositories.commandRepo import CommandRepository


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx, command_name: str = ""):
        try:
            if command_name:
                cmd = CommandRepository.get_command(command_name)
                if cmd:
                    embed = discord.Embed(
                        title=f"📘 Help: `{cmd[0]}`",
                        description=cmd[1] or "No description provided.",
                        color=discord.Color.blurple(),
                    )
                    embed.add_field(
                        name="Category", value=cmd[4] or "General", inline=True
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(
                        f"❌ No command found with the name `{command_name}`."
                    )
                return

            all_commands = CommandRepository.get_all_commands()
            if not all_commands:
                await ctx.send("No commands found in the database.")
                return

            categories = {}
            for cmd in all_commands:
                category = cmd[4] or "General"
                categories.setdefault(category, []).append(cmd)

            embed = discord.Embed(
                title="📘 Shellmates Bot Commands",
                description="Here are all available commands grouped by category:",
                color=discord.Color.green(),
            )

            for category, cmds in categories.items():
                cmd_list = "\n".join(
                    [f"`{c[0]}` - {c[1] or 'No description'}" for c in cmds]
                )
                embed.add_field(name=f"📂 {category}", value=cmd_list, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Error loading help: {e}")
            print(f"[HelpCommands Error] {e}")


async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
