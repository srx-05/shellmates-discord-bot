import discord
from discord.ext import commands
from database.Repositories.bannedwordRepo import BannedWordRepository


ALLOWED_ROLES = ["Admin", "Mod"]


class BannedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = BannedWordRepository()

    # -----------------------------------------------------------------
    def has_allowed_role(self, user_roles):
        allowed_lower = [r.lower() for r in ALLOWED_ROLES]
        return any(role.name.lower() in allowed_lower for role in user_roles)

    # -----------------------------------------------------------------
    @commands.command(name="banword")
    async def ban_word(self, ctx, *, word: str):
        """Add a word to the banned list."""
        if not self.has_allowed_role(ctx.author.roles):
            return await ctx.send("❌ You don't have permission to ban words.")

        if self.repo.exists_banned_word(word):
            return await ctx.send(f"⚠️ `{word}` is already banned.")

        self.repo.add_banned_word(word)
        await ctx.send(f"✅ `{word}` has been added to the banned words list.")

    # -----------------------------------------------------------------
    @commands.command(name="unbanword")
    async def unban_word(self, ctx, *, word: str):
        """Remove a word from the banned list."""
        if not self.has_allowed_role(ctx.author.roles):
            return await ctx.send("❌ You don't have permission to unban words.")

        self.repo.delete_banned_word(word)
        await ctx.send(f"🗑️ `{word}` has been removed from the banned words list.")

    # -----------------------------------------------------------------
    @commands.command(name="listbanned")
    async def list_banned(self, ctx):
        """Show all banned words."""
        words = self.repo.get_all_banned_words()
        if not words:
            return await ctx.send("⚠️ No banned words yet.")

        word_list = ", ".join(
            w[1] for w in words
        )  # assuming columns: (id, word, created_at)
        await ctx.send(f"📜 **Banned Words:** {word_list}")

    # -----------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        """Auto-delete messages containing banned words."""
        if message.author.bot:
            return

        banned_found = self.repo.find_banned_words_in_text(message.content)
        if banned_found:
            try:
                await message.delete()
                await message.channel.send(
                    f"⚠️ {message.author.mention}, your message contained banned word(s): "
                    f"{', '.join(banned_found)}",
                    delete_after=5,
                )
            except discord.Forbidden:
                print(
                    f"[ERROR] Missing permission to delete messages in #{message.channel}"
                )
            except discord.HTTPException as e:
                print(f"[ERROR] Failed to delete message: {e}")


async def setup(bot):
    await bot.add_cog(BannedWords(bot))
