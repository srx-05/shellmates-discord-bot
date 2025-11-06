import discord
from discord.ext import commands
from database.Repositories.commandRepo import CommandRepository

ALLOWED_ROLES = ["Mod", "Admin"]


class CommandManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = CommandRepository()

    def has_allowed_role(self, user_roles):

        allowed_lower = [role.lower() for role in ALLOWED_ROLES]
        return any(role.name.lower() in allowed_lower for role in user_roles)

    @commands.command(name="add_command")
    async def add_command(
        self, ctx, name: str, category: str = "General", *, description: str = ""
    ):
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission to add commands.")
            return

        try:
            if self.repo.command_exists(name):
                await ctx.send(f"⚠️ Command `{name}` already exists.")
                return

            self.repo.create_command(name, description, category)
            await ctx.send(f"✅ Command `{name}` added successfully!")
        except Exception as e:
            await ctx.send(f"❌ Failed to add command: {e}")

    @commands.command(name="update_command")
    async def update_command(self, ctx, name: str, *, description: str):
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission to update commands.")
            return

        try:
            if not self.repo.command_exists(name):
                await ctx.send(f"⚠️ Command `{name}` does not exist.")
                return

            self.repo.update_command(name, description)
            await ctx.send(f"📝 Command `{name}` updated successfully!")
        except Exception as e:
            await ctx.send(f"❌ Failed to update command: {e}")

    @commands.command(name="delete_command")
    async def delete_command(self, ctx, name: str):
        if not self.has_allowed_role(ctx.author.roles):
            await ctx.send("❌ You don't have permission to delete commands.")
            return

        try:
            if not self.repo.command_exists(name):
                await ctx.send(f"⚠️ Command `{name}` does not exist.")
                return

            self.repo.delete_command(name)
            await ctx.send(f"🗑️ Command `{name}` deleted successfully!")
        except Exception as e:
            await ctx.send(f"❌ Failed to delete command: {e}")


async def setup(bot):
    await bot.add_cog(CommandManagement(bot))
