import discord
from discord.ext import commands
import os
import yt_dlp as youtube_dl

intents = discord.Intents.default()
intents.all()
intents.message_content = True
queue = []
loop_enabled = False
paused = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(">> Logged in as {0.user}".format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send(f"{round(bot.latency*1000)}(ms)")

@bot.command()
async def hi(ctx):
    await ctx.send("Nöfnöf!")

@bot.command()
async def sayd(ctx, *, msg):
    await ctx.send(msg)

@bot.command()
async def play(ctx, *, query: str):
    global url, title, queue, loop_enabled, paused
    # disconnect from the current voice channel
    voice_client = ctx.message.guild.voice_client
    channel = ctx.author.voice.channel
    # error handling
    try:
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    except:
        await ctx.send("You are not in a voice channel.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
        "cachedir": False, # Disable caching
        'noplaylist': True, # Only download single song, not playlist
        'nocheckcertificate': True, # Suppress HTTPS certificate validation
        'ignoreerrors': True, # Suppress "ERROR: unable to download video" warnings
        'no_warnings': True, # Suppresses the "ERROR: video unavailable" warning
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            # Attempt to extract info from URL
            info_dict = ydl.extract_info(query, download=False)
            url = info_dict.get('url')
            title = info_dict.get('title')
            if not url:
                raise ValueError("URL extraction failed.")
        except Exception as e:
            print(f"Exception: {e}")
            # If URL extraction fails, treat as a search query
            search_result = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            if search_result is None:
                await ctx.send("No results found.")
                return
            url = search_result.get('url')
            title = search_result.get('title')
            if not url:
                await ctx.send(f"No results found for {query}.")
                return
    try:
        voice_channel = await channel.connect()
    except:
        pass
    queue.append({"url": url, "title": title})
    try:
        video_lenght = float(info_dict['duration']) # this only works if a url is used in !play. To get the duration of a search result, we need to use the search_result variable
    except:
        video_lenght = None
    # declare duration hour and minute as empty variables
    duration_hours = 0
    duration_minutes = 0
    if video_lenght is not None:
        video_length = float(video_lenght)
        # if enough length for hours
        if video_length >= 3600:
            duration_hours = int(video_length // 3600)
        # if enough length for minutes
        if video_length >= 60:
            duration_minutes = int(video_length // 60)
        duration_seconds = int(video_length % 60)
        await ctx.send(f"Added {title} to the queue. Duration: {duration_hours}h {duration_minutes}m {duration_seconds}s  -  {len(queue)} songs currently in queue.")
        # await ctx.send(f"Added {title} to the queue. Duration: {video_lenght//60}m {video_lenght%60}s  -  {len(queue)} songs currently in queue.")    
    else:
        await ctx.send(f"Added {title} to the queue. Duration: Unknown  -  {len(queue)} songs currently in queue.")
    if not ctx.voice_client.is_playing() and not paused:
        await play_next(ctx)


async def play_next(ctx):
    global queue, loop_enabled
    # check if queue is not empty
    if len(queue) > 0:
        # get the first song in the queue
        song = queue[0]
        url = song["url"]
        title = song["title"]
        # remove the first song from the queue
        queue = queue[1:]
        # play the song
        FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
        }
        voice_client = ctx.message.guild.voice_client
        try:
            # Use the after parameter to call a function when the song finishes playing
            voice_client.play(discord.FFmpegOpusAudio(url, **FFMPEG_OPTIONS), after=lambda e: bot.loop.create_task(after_play(ctx, url, title)))
            await ctx.send(f"Now playing {title}")
        except Exception as e:
            print(f"Exception: {e}")
            await ctx.send(f"Error: {e}")

async def after_play(ctx, url, title):
    global loop_enabled, queue
    if loop_enabled:
        queue.append({"url": url, "title": title})
    await play_next(ctx)

@bot.command()
async def showqueue(ctx):
    global queue
    if len(queue) > 0:
        queue_list = "\n".join([f"{i+1}: {song['title']}" for i, song in enumerate(queue)])
        await ctx.send(f"Current queue:\n{queue_list}")
    else:
        await ctx.send("Queue is empty.")

@bot.command()
async def skip(ctx):
    global paused
    voice_client = ctx.message.guild.voice_client
    if paused:
        paused = False
        voice_client.resume()
    if voice_client.is_playing():
        voice_client.stop()
        await play_next(ctx)
    else:
        await ctx.send("No song is playing.")

@bot.command()
async def url(ctx):
    if url != "":
        if ctx.author.guild_permissions.administrator:
            await ctx.send(url)
        else:
            await ctx.send("You are not an admin.")
    else:
        await ctx.send("No url.")

@bot.command()
async def clear(ctx):
    # check if any song is playing
    global queue, loop_enabled, url, title
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        queue = []
        loop_enabled = False
        url = ""
        title = ""
        await ctx.send("Queue cleared.")
    else:
        await ctx.send("No song is playing.")


# loop command, takes the current song and plays it on loop
@bot.command()
async def loop(ctx):
    global loop_enabled
    loop_enabled = not loop_enabled
    await ctx.send(f"Looping is now {'enabled' if loop_enabled else 'disabled'}.")

# leave command
@bot.command()
async def leave(ctx):
    global url
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    # reset the url and playing status
    await ctx.send("Disconnected.")

bot.remove_command('help')

@bot.command()
async def help(ctx):
    await ctx.send("```!hi\n!ping\n!sayd [message]\n!play [url]\nplay a song from youtube using url (more accurate)\n!play [song name]\nplay song from youtube using search term (less accurate)\n!loop\nloop the current song\n!showqueue\n!skip\n!pause\npause and unpause the current song\n!leave```")

@bot.command()
async def clearchat(ctx, amount=5):
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.send("You are not an admin.")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def pause(ctx):
    global paused, queue
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing() and not paused:
        voice_client.pause()
        paused = True
        await ctx.send("Paused.")
    elif paused:
        voice_client.resume()
        paused = False
        await ctx.send("Resumed.")
    else:
        await ctx.send("No song is playing.")


# command ideas:
# !shuffle
# !np, !nowplaying
# !shuffle
# !remove
# !move
# !lyrics
# !search
# !join
# !disconnect
# !stop
# !restart
# !seek
# !forward
# !rewind
# !random
        
# stops the bot, making it offline
@bot.command()
async def stop(ctx):
    if ctx.author.guild_permissions.administrator:
        print(f"Bot turned off by {ctx.author}.")
        await bot.close()
        # after the bot is stopped, the bot will print "Bot is offline."
    else:
        await ctx.send("You are not an admin.")


token = open("token.txt", "r")
bot.run(token.read())