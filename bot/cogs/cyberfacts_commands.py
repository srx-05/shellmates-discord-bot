import discord
from discord.ext import commands
from database.Repositories.factRepo import FactRepository


class CyberFacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = FactRepository()

    # --------------------------------------------------------------------------
    # /cyberfact — show random fact
    # --------------------------------------------------------------------------
    @commands.hybrid_command(name="cyberfact", description="Show a random cybersecurity fact")
    async def cyberfact(self, ctx):
        fact = self.repo.get_random_fact()
        if fact:
            await ctx.send(f"💡 {fact[1]}")
        else:
            await ctx.send("No cybersecurity facts found in the database!")

    # --------------------------------------------------------------------------
    # /addcyberfact — interactive admin-only guided flow
    # --------------------------------------------------------------------------
    @commands.hybrid_command(name="addcyberfact", description="Add a new cybersecurity fact (admins only, guided flow)")
    async def addcyberfact(self, ctx):
        # --- Permission check ---
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ You don't have permission to use this command.")
            return

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(
            "🧠 Let's add a new cybersecurity fact!\n"
            '👉 Please **type the fact content** surrounded by **double quotes**, for example:\n'
            '"The first worm to spread via email appeared in 1999."'
            '\nOr type **abort** to cancel.'
        )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=120)
        except TimeoutError:
            await ctx.send("⏳ Time’s up — please start again when ready.")
            return

        if msg.content.lower() == "abort":
            await ctx.send("❌ Operation aborted.")
            return

        # --- Extract fact content ---
        content = msg.content.strip()
        if not (content.startswith('"') and content.endswith('"')):
            await ctx.send("⚠️ Please surround the fact with double quotes. Try again later.")
            return
        content = content[1:-1]  # remove quotes

        # --- Ask for source_type ---
        await ctx.send(
            "📚 Now, specify the **source type** (`user` or `external`).\n"
            "Or type **abort** to cancel."
        )
        msg2 = await self.bot.wait_for("message", check=check, timeout=60)
        if msg2.content.lower() == "abort":
            await ctx.send("❌ Operation aborted.")
            return

        source_type = msg2.content.lower().strip()
        if source_type not in ("user", "external"):
            await ctx.send("⚠️ Invalid source type. Must be `user` or `external`. Operation cancelled.")
            return

        # --- Ask for source_url if external ---
        source_url = None
        if source_type == "external":
            await ctx.send(
                "🌐 Please provide the **source URL** (link to article/reference). "
                "Or type **none** if not available, or **abort** to cancel."
            )
            msg3 = await self.bot.wait_for("message", check=check, timeout=60)
            if msg3.content.lower() == "abort":
                await ctx.send("❌ Operation aborted.")
                return
            source_url = None if msg3.content.lower() == "none" else msg3.content.strip()

        added_by = str(ctx.author.id)

        try:
            new_fact = self.repo.add_fact(content, source_type, source_url, added_by)
            if new_fact:
                await ctx.send("✅ Cyber fact successfully added to the database!")
            else:
                await ctx.send("⚠️ Failed to add the cyber fact.")
        except Exception as e:
            print(f"[ERROR] addcyberfact: {e}")
            await ctx.send("❌ An error occurred while adding the cyber fact.")


async def setup(bot):
    await bot.add_cog(CyberFacts(bot))

