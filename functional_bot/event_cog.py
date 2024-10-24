from discord.ext.commands import command
from config.config import random, asyncio, discord
from discord.ext import commands
"""
Покіщо врозробці концепції
1) black_jack
2)???
"""

# Покіщо нічого не готово
class event_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="jack", description="Розпочати гру в Blackjack")
    async def black_jack(self, ctx):
        await ctx.respond(f"{ctx.author.mention}, розпочинаємо гру в Blackjack!", ephemeral=True)
        await self.start_blackjack(ctx)

    async def start_blackjack(self, ctx):
        cards = []

        for card in cards:
            with open(f"./cards/{card}", "rb") as f:
                picture = discord.File(f)
                await ctx.respond(file=picture, ephemeral=True)

        await ctx.respond(f"Твоя початкова рука. Хочеш взяти ще одну карту?", ephemeral=True)