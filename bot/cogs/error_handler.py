import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Global error handler for all commands"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"⚠️ Missing argument: `{error.param.name}`")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have the required permissions.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ You can't use this command.")
        else:
            print(f"Unhandled error: {error}")
            await ctx.send("❌ An unexpected error occurred. Please contact the admin.")


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
