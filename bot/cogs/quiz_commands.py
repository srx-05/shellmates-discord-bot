# import random
# import asyncio
# import discord
# from discord.ext import commands
# # from utils.database import db  # assuming you already have db connection setup

# class Quiz(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         # self.collection = db.quiz_scores  # MongoDB collection for scores

#         # Example cybersecurity questions
#         self.questions = [
#             {
#                 "question": "What does 'VPN' stand for?",
#                 "options": ["Virtual Private Network", "Verified Personal Node", "Virtual Protected Net", "Variable Path Network"],
#                 "answer": 0
#             },
#             {
#                 "question": "What is phishing?",
#                 "options": ["An email scam to steal information", "A firewall setting", "A secure encryption protocol", "A type of malware"],
#                 "answer": 0
#             },
#             {
#                 "question": "What is the strongest password?",
#                 "options": ["password123", "qwerty", "IloveCats!", "R@nd0m#P@55!"],
#                 "answer": 3
#             },
#             {
#                 "question": "What year was the first computer virus created?",
#                 "options": ["1986", "1999", "1975", "2003"],
#                 "answer": 0
#             },
#         ]

#     # --- Utility ---
#     async def add_points(self, user_id: int, points: int):
#         self.collection.update_one(
#             {"user_id": user_id},
#             {"$inc": {"points": points}},
#             upsert=True
#         )

#     async def get_leaderboard(self, limit=10):
#         return list(self.collection.find().sort("points", -1).limit(limit))

#     # --- Commands ---
#     @commands.command(name="quiz", help="Answer a cybersecurity quiz question to earn points!")
#     async def quiz(self, ctx):
#         question = random.choice(self.questions)
#         options = question["options"]
#         correct_index = question["answer"]

#         embed = discord.Embed(
#             title="🧠 Cybersecurity Quiz",
#             description=question["question"],
#             color=discord.Color.blurple()
#         )

#         for i, option in enumerate(options):
#             embed.add_field(name=f"{i+1}.", value=option, inline=False)

#         embed.set_footer(text="Type the number of your answer (e.g., 1, 2, 3, or 4). You have 15 seconds!")
#         await ctx.send(embed=embed)

#         def check(msg):
#             return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

#         try:
#             msg = await self.bot.wait_for("message", check=check, timeout=15)
#         except asyncio.TimeoutError:
#             await ctx.send("⏰ Time’s up! Better luck next time.")
#             return

#         user_answer = int(msg.content) - 1
#         if user_answer == correct_index:
#             await self.add_points(ctx.author.id, 10)
#             await ctx.send(f"✅ Correct! You earned **10 points**, {ctx.author.mention}!")
#         else:
#             correct_option = options[correct_index]
#             await ctx.send(f"❌ Wrong! The correct answer was **{correct_option}**.")

#     @commands.command(name="leaderboard", help="Show the top quiz players.")
#     async def leaderboard(self, ctx):
#         leaderboard = await self.get_leaderboard()
#         if not leaderboard:
#             await ctx.send("No one has played yet. Be the first to take the quiz!")
#             return

#         embed = discord.Embed(
#             title="🏆 Cyber Quiz Leaderboard",
#             color=discord.Color.gold()
#         )

#         for i, entry in enumerate(leaderboard, start=1):
#             user = await self.bot.fetch_user(entry["user_id"])
#             embed.add_field(
#                 name=f"{i}. {user.name}",
#                 value=f"{entry['points']} points",
#                 inline=False
#             )

#         await ctx.send(embed=embed)

# async def setup(bot):
#     await bot.add_cog(Quiz(bot))
# s