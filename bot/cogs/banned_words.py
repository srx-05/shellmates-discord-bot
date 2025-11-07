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
    @commands.command(
        name="banword", help="Add a word to the banned list (Admin/Mod only)"
    )
    async def ban_word(self, ctx, *, word: str):
        """Add a word to the banned list."""
        if not self.has_allowed_role(ctx.author.roles):
            return await ctx.send("❌ You don't have permission to ban words.")

        # Validate input
        word = word.strip().lower()
        if len(word) < 2:
            return await ctx.send("❌ Word must be at least 2 characters long.")

        if self.repo.exists_banned_word(word):
            return await ctx.send(f"⚠️ `{word}` is already banned.")

        self.repo.add_banned_word(word)
        await ctx.send(f"✅ `{word}` has been added to the banned words list.")

    # -----------------------------------------------------------------
    @commands.command(
        name="unbanword", help="Remove a word from the banned list (Admin/Mod only)"
    )
    async def unban_word(self, ctx, *, word: str):
        """Remove a word from the banned list."""
        if not self.has_allowed_role(ctx.author.roles):
            return await ctx.send("❌ You don't have permission to unban words.")

        word = word.strip().lower()
        if not self.repo.exists_banned_word(word):
            return await ctx.send(f"⚠️ `{word}` is not in the banned words list.")

        self.repo.delete_banned_word(word)
        await ctx.send(f"🗑️ `{word}` has been removed from the banned words list.")

    # -----------------------------------------------------------------
    @commands.command(name="listbanned", help="Show all banned words")
    async def list_banned(self, ctx):
        """Show all banned words."""
        words = self.repo.get_all_banned_words()
        if not words:
            return await ctx.send("⚠️ No banned words yet.")

        # Create a paginated list if there are many words
        word_list = ", ".join(w[1] for w in words)

        if len(word_list) > 1900:  # Discord message limit
            word_list = word_list[:1900] + "..."

        embed = discord.Embed(
            title="📜 Banned Words", description=word_list, color=discord.Color.red()
        )
        embed.set_footer(text=f"Total: {len(words)} words")
        await ctx.send(embed=embed)

    # -----------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        """Auto-delete messages containing banned words."""
        if message.author.bot:
            return

        # Don't check messages from users with allowed roles
        if self.has_allowed_role(message.author.roles):
            return

        banned_found = self.repo.find_banned_words_in_text(message.content)
        if banned_found:
            try:
                await message.delete()
                warning_msg = await message.channel.send(
                    f"⚠️ {message.author.mention}, your message contained banned word(s): "
                    f"`{', '.join(banned_found)}`",
                    delete_after=5,
                )
                print(
                    f"🚫 Deleted message from {message.author} containing banned words: {banned_found}"
                )
            except discord.Forbidden:
                print(f"❌ Missing permission to delete messages in #{message.channel}")
            except discord.HTTPException as e:
                print(f"❌ Failed to delete message: {e}")

    # -----------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Also check edited messages for banned words."""
        if after.author.bot:
            return

        # Don't check messages from users with allowed roles
        if self.has_allowed_role(after.author.roles):
            return

        # Only check if content actually changed
        if before.content != after.content:
            banned_found = self.repo.find_banned_words_in_text(after.content)
            if banned_found:
                try:
                    await after.delete()
                    await after.channel.send(
                        f"⚠️ {after.author.mention}, your edited message contained banned word(s): "
                        f"`{', '.join(banned_found)}`",
                        delete_after=5,
                    )
                    print(
                        f"🚫 Deleted edited message from {after.author} containing banned words: {banned_found}"
                    )
                except discord.Forbidden:
                    print(
                        f"❌ Missing permission to delete messages in #{after.channel}"
                    )
                except discord.HTTPException as e:
                    print(f"❌ Failed to delete edited message: {e}")


async def setup(bot):
    await bot.add_cog(BannedWords(bot))
