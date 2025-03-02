from config.config import BOT_TOKEN
from functional_bot.help_cog import help_cog
from music.music_cog import Music
from functional_bot.text_cog import text_cog
import asyncio
import discord.ext.commands as commands
import discord

#стартова командна строка
BOT_PREFIX = "."

#дозволи для бота
intents = discord.Intents.all()

#ініціалізація бота
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Видаляємо стандартну команду допомоги, щоб створити власну
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' in: ({channel})")

    await bot.process_commands(message)  # Важливо: дає змогу обробляти команди


# Подія для закриття сесії, коли бот вимикається
@bot.event
async def on_shutdown():
    print("Bot is shutting down.")
    await bot.close()


async def start_bot():
    await bot.login(BOT_TOKEN)
    # Додаємо когі
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(Music(bot))
    await bot.add_cog(text_cog(bot))
    # Запускаємо бота
    try:
        await bot.start(BOT_TOKEN)  # запуск сесії
    finally:
        await bot.close()  # закриття сесії


# Запускаємо бота
asyncio.run(start_bot())
