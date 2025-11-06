import discord
from discord.ext import commands
from database.Repositories.factRepo import FactRepository


class CyberFact(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command(name="cyberfact")
    async def cyberfact(self, ctx):
        try:
            fact = FactRepository.get_random_fact()
            if fact:
                content = fact[1]
                source_url = fact[3]
                message = f"💡 {content}"
                if source_url:
                    message += f"\n🔗 Source: {source_url}"
                await ctx.send(message)
            else:
                await ctx.send("⚠️ No cyber facts found in the database yet.")
        except Exception as e:
            print(f"[ERROR] cyberfact command: {e}")
            await ctx.send("❌ An error occurred while fetching a cyber fact.")


async def setup(bot):
    await bot.add_cog(CyberFact(bot))
