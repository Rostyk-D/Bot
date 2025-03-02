from discord.ext import commands
from config.config import asyncio, discord, yt_dlp
# import spotipy

"""
Не готове повністю: 30%/100%
1) Youtube music +
2) Spotify music -
3) SoundCloud music - 
"""
YDL_OPTION = {  #  Youtube settings
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,  # для того щоби не тратити інтернет на перевірку + скіп перевірки по можливості
    'no_warnings': True,  # оминати попередження (хз чи працює)
    'default_search': 'auto',
    'socket_timeout': 30,  # затримка для сокета через те що інтернет поганий
}

FFMPEG_OPTION = {  # Setting for audio player
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  # reconnection
    'options': '-vn -b:a 196k'  # 128 low or 196 high
}

# oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
# token_dict = oauth_object.get_access_token()
# token = token_dict['access_token']
# spotifyObject = spotipy.Spotify(auth=token)
# user_name = spotifyObject.current_user()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command(name='play', aliases=["p"])
    async def queue(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            await ctx.send('Ви не підключені до голосового каналу!')
            return

        permissions = voice_channel.permissions_for(ctx.guild.me)
        if not permissions.connect or not permissions.speak:
            await ctx.send('Мені потрібні дозволи на підключення та говоріння у голосовому каналі!')
            return

        if not ctx.voice_client:
            try:
                await voice_channel.connect()
            except Exception as e:
                print(f"Не вдалося підключитися: {e}")
                await ctx.send(f"Не вдалося підключитися: {e}")
                return

        async with ctx.typing():
            try:
                with yt_dlp.YoutubeDL(YDL_OPTION) as ydl:
                    info = ydl.extract_info(f"ytsearch:{search}", download=False)
                    if 'entries' in info:
                        info = info['entries'][0]
                        url = info['url']
                        title = info['title']
                        self.queue.append((url, title))
                        await ctx.send(f"Додано до черги: {title}")
            except Exception as e:
                await ctx.send(f"Помилка: {e}")
                return

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            try:
                source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTION)
                ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
                await ctx.send(f"Зараз грає: {title}")
            except Exception as e:
                await ctx.send(f"Помилка під час відтворення аудіо: {e}")
                await self.play_next(ctx)
        else:
            await ctx.send('Черга порожня!')

    @commands.command(name='skip')
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Пропущено поточний трек")

    @commands.command(name='queue', aliases=["q"])
    async def show_queue(self, ctx):
        if not self.queue:
            await ctx.send("Черга порожня.")
            return

        queue_list = [f"{index + 1}. {title}" for index, (_, title) in enumerate(self.queue)]
        await ctx.send("Поточна черга:\n" + "\n".join(queue_list))

    @commands.command(name='remove')
    async def remove(self, ctx, index: int):
        if 0 <= index < len(self.queue):
            removed_song = self.queue.pop(index)
            await ctx.send(f'Видалено пісню: {removed_song[1]} з черги.')
        else:
            await ctx.send('Невірний індекс! Вкажіть правильний індекс.')

    @commands.command(name='clean')
    async def clear(self, ctx):
        self.queue.clear()
        await ctx.send('Черга очищена!')

    @commands.command(name='pause')
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Відтворення призупинено.")
        else:
            await ctx.send("Наразі нічого не грає!")

    @commands.command(name='resume')
    async def resume(self, ctx):
        if ctx.voice_client and not ctx.voice_client.is_playing():
            ctx.voice_client.resume()
            await ctx.send("Відтворення відновлено.")
        else:
            await ctx.send("Відтворення вже триває або я не в голосовому каналі!")

    @commands.command(name="l")
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send("Відключено від голосового каналу.")
        else:
            await ctx.send("Я не в голосовому каналі.")