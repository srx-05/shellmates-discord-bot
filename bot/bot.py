import discord
from discord.ext import commands
import logging
from config import Config



logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix=Config.COMMAND_PREFIX,
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )
    
    async def setup_hook(self):
        # # Connect to MongoDB
        # try:
        #     db.connect()
        #     logger.info("✓ Database connected")
        # except Exception as e:
        #     logger.error(f"✗ Failed to connect to database: {e}")
        #     raise
        
        # Load cogs
        await self.load_cogs()
    
    async def load_cogs(self):
        cogs = [
            'bot.cogs.cyberfacts_commands',
            'bot.cogs.help_commands',
            'bot.cogs.events_commands',
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"✓ Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"✗ Failed to load cog {cog}: {e}")
    
    async def on_ready(self):
        logger.info(f"✓ Bot is ready! Logged in as {self.user}")
        logger.info(f"✓ Connected to {len(self.guilds)} guilds")
        

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found. Use `!help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        else:
            logger.error(f"Error in command {ctx.command}: {error}")
            await ctx.send("❌ An error occurred while processing the command.")
    
    async def close(self):
        # db.close()
        await super().close()