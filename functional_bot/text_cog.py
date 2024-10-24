from config.config import random, asyncio, discord
from discord.ext import commands

class text_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["c"], help="Clear chat")
    async def clear(self, ctx, amount: str = ""):
        if isinstance(ctx.channel, discord.TextChannel):
            if amount.lower() == "all":
                messages = []  # массив повідомленнь
                async for message in ctx.channel.history(limit=None):  # Збираєм всі повідомлення з чату
                    messages.append(message)
                for chunk in [messages[i:i + 100] for i in range(0, len(messages), 100)]:
                    try:
                        await ctx.channel.delete_messages(chunk)
                    except discord.HTTPException as e:
                        error_message = await ctx.send(f"Помилка видалення повідомлення: {e}")
                        await asyncio.sleep(3)
                        await error_message.delete()
                        await ctx.message.delete()
                    await asyncio.sleep(5)
                success_message = await ctx.send('Всі повідомлення видаленні, до давності 14 днів.') # правила діскорду
                await asyncio.sleep(3)
                await success_message.delete()
            elif amount.isdigit():
                amount = int(amount)
                if amount >= 0:
                    if isinstance(ctx.author, discord.Member) and ctx.author.guild_permissions.manage_messages:
                        await ctx.channel.purge(limit=amount + 1)
                        success_message = await ctx.send(f'Удалено {amount} сообщений.', delete_after=5)
                    else:
                        error_message = await ctx.send("У вас нема прав на видалення повідомленнь.")
                        await asyncio.sleep(5)
                        await error_message.delete()
                        await ctx.message.delete()
            else:
                error_message = await ctx.send("Неправильное число. Используйте `!clear all` или укажите целое число, например: `!clear 3`.")
                await asyncio.sleep(5)
                await error_message.delete()
                await ctx.message.delete()
        else:
            await ctx.send("Ця команда не для ЛС!")

    @commands.command(name="roll", help="бере рандомне число")
    async def roll(self, ctx, start: int, end: int):
        if isinstance(ctx.channel, discord.TextChannel):  # Перевірка, чи канал - TextChannel
            try:
                if start < end:
                    result = random.randint(start, end)
                    await ctx.send(f'Рандомне число від {start} до {end}: {result}')
                else:
                    error_message = await ctx.send("Початкове число повинно бути менше за кінцеве.")
                    await asyncio.sleep(7)  # Затримка на 7 секунд
                    await error_message.delete()  # Видалення повідомлення про помилку
                    await ctx.message.delete()  # Видалення повідомлення користувача
            except ValueError:
                error_message = await ctx.send("Некоректний ввід. Введіть числа.")
                await asyncio.sleep(7)  # Затримка на 7 секунд
                await error_message.delete()  # Видалення повідомлення про помилку
                await ctx.message.delete()  # Видалення повідомлення користувача
        else:
            error_message = await ctx.send("Ця команда не для ЛС!!!")
            await asyncio.sleep(7)  # Затримка на 7 секунд
