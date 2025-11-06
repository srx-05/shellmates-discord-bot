import json
import random
import asyncio
import discord
from discord.ext import commands
from database.Repositories.quizRepo import QuizRepository
from database.Repositories.userRepo import UserRepository
from database.connection import Database


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = UserRepository()

    # --------------------------------------------------------------------------
    # /quiz [difficulty]
    # --------------------------------------------------------------------------
    @commands.command(
        name="quiz",
        help="Take a quiz! Optionally choose a difficulty (easy, medium, hard).",
    )
    async def quiz(self, ctx, difficulty: str = ""):
        valid_difficulties = ["easy", "medium", "hard"]

        # Auto-register user if not exists
        self.repo.ensure_user(ctx.author.id, ctx.author.name)

        if difficulty and difficulty.lower() not in valid_difficulties:
            await ctx.send(
                f"⚠️ Invalid difficulty. Choose from: {', '.join(valid_difficulties)}."
            )
            return

        quiz = QuizRepository.fetch_random_quiz(
            difficulty.lower() if difficulty else None
        )
        if not quiz:
            await ctx.send("❌ No quiz found for that difficulty.")
            return

        quiz_id, fact_id, question, correct_answer, wrong_answers, diff, *_ = quiz

        # Parse wrong answers
        try:
            if isinstance(wrong_answers, str):
                wrong_answers = json.loads(wrong_answers)
        except Exception:
            wrong_answers = wrong_answers.split(",") if wrong_answers else []

        # Prepare options
        options = wrong_answers + [correct_answer]
        random.shuffle(options)
        correct_index = options.index(correct_answer)

        # Create embed
        embed = discord.Embed(
            title=f"🧠 Quiz Time! (Difficulty: {diff.capitalize()})",
            description=question,
            color=discord.Color.blurple(),
        )
        for i, opt in enumerate(options, start=1):
            embed.add_field(name=f"{i}.", value=opt, inline=False)

        embed.set_footer(
            text="Type the number of your answer (1, 2, 3...) — you have 15 seconds!"
        )
        await ctx.send(embed=embed)

        # Wait for answer
        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.isdigit()
                and 1 <= int(msg.content) <= len(options)
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=15)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time’s up!")
            self.save_result(ctx.author.id, quiz_id, False, 0)
            return

        user_answer = int(msg.content) - 1
        is_correct = user_answer == correct_index
        points_earned = self.calculate_points(diff, is_correct)

        if is_correct:
            await ctx.send(
                f"✅ Correct, {ctx.author.mention}! You earned **{points_earned} points!**"
            )
        else:
            await ctx.send(f"❌ Wrong! The correct answer was **{correct_answer}**.")

        # Save result + update points
        self.save_result(ctx.author.id, quiz_id, is_correct, points_earned)
        if is_correct and points_earned > 0:
            self.add_points(ctx.author.id, points_earned, "Quiz correct answer")

    # --------------------------------------------------------------------------
    # Utilities for saving results and updating points
    # --------------------------------------------------------------------------
    def calculate_points(self, difficulty, correct):
        if not correct:
            return 0
        base = {"easy": 5, "medium": 10, "hard": 20}
        return base.get(difficulty, 10)

    def save_result(self, user_id, quiz_id, is_correct, points_earned):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO quiz_results (user_id, quiz_id, is_correct, points_earned)
            VALUES (%s, %s, %s, %s);
            """,
            (str(user_id), quiz_id, is_correct, points_earned),
        )
        conn.commit()
        cur.close()
        db.return_connection(conn)

    def add_points(self, user_id, points, reason):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        # Ensure user exists
        cur.execute("SELECT user_id FROM users WHERE user_id = %s;", (str(user_id),))
        user = cur.fetchone()
        if not user:
            cur.execute(
                """
                INSERT INTO users (user_id, username, joined_at, points, level)
                VALUES (%s, %s, NOW(), 0, 1)
                ON CONFLICT (user_id) DO NOTHING;
                """,
                (str(user_id), "Unknown"),
            )

        # Update points
        cur.execute(
            "UPDATE users SET points = points + %s WHERE user_id = %s;",
            (points, str(user_id)),
        )

        # Add to history
        cur.execute(
            """
            INSERT INTO points_history (user_id, reason, points_added)
            VALUES (%s, %s, %s);
            """,
            (str(user_id), reason, points),
        )

        conn.commit()
        cur.close()
        db.return_connection(conn)

    # --------------------------------------------------------------------------
    # /leaderboard command
    # --------------------------------------------------------------------------
    @commands.command(
        name="leaderboard", help="Show the top players based on quiz points."
    )
    async def leaderboard(self, ctx):
        # Ensure the user exists before showing leaderboard
        self.repo.ensure_user(ctx.author.id, ctx.author.name)

        top_users = self.repo.get_top_users(limit=10)

        if not top_users:
            await ctx.send(
                "No one has earned points yet. Be the first to take the quiz!"
            )
            return

        embed = discord.Embed(
            title="🏆 Quiz Leaderboard",
            description="Top players ranked by total points",
            color=discord.Color.gold(),
        )

        for i, (username, points, level) in enumerate(top_users, start=1):
            embed.add_field(
                name=f"{i}. {username}",
                value=f"⭐ {points} points — Level {level}",
                inline=False,
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Quiz(bot))
