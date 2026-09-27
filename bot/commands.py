import asyncio
from discord.ext import commands
from bot.music import extract_song, get_player, play_song
from bot.help import MusicHelpCommand
from bot.info import BOT_INFO


def setup_commands(bot: commands.Bot) -> None:
    bot.help_command = MusicHelpCommand()


    @bot.command(help="Check bot latency.")
    async def ping(ctx):
        await ctx.send(f"{round(bot.latency * 1000)} ms")


    @bot.command(help="nöf")
    async def hi(ctx):
        await ctx.send("Oink!")


    @bot.command(hidden=True)
    async def testplayer(ctx):
        player = get_player(ctx.guild.id)

        player.add_to_queue({"title": "Test Song"})

        await ctx.send(
            f"Queue now contains {len(player.queue)} song(s)."
        )


    @bot.command(help="Join your voice channel.", hidden=True)
    @commands.has_permissions(administrator=True)
    async def join(ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel.")
            return

        channel = ctx.author.voice.channel
        player = get_player(ctx.guild.id)

        if ctx.voice_client is not None:
            if ctx.voice_client.channel == channel:
                await ctx.send("Klinoff is already in your voice channel.")
                return

            await ctx.voice_client.move_to(channel)
            player.voice_client = ctx.voice_client
        else:
            player.voice_client = await channel.connect()

        await ctx.send(f"Joined **{channel.name}**.")


    @bot.command(help="Play a song.")
    async def play(ctx, *, query: str):
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel.")
            return

        player = get_player(ctx.guild.id)

        song = extract_song(query)

        if song is None:
            await ctx.send("I couldn't find that song.")
            return

        player.add_to_queue(song)

        if song.duration is not None:
            minutes, seconds = divmod(song.duration, 60)
            duration = f"{minutes}:{seconds:02d}"
        else:
            duration = "Unknown"

        await ctx.send(
            f"Added **{song.title}** to the queue.\n"
            f"Duration: `{duration}`\n"
            f"Position: `{len(player.queue)}`"
        )

        if player.voice_client is None:
            player.voice_client = await ctx.author.voice.channel.connect()

        if not player.voice_client.is_playing() and not player.paused:
            success = await play_song(player, bot)
            if not success:
                await ctx.send("I couldn't play the song...")


    @bot.command(help="Show the current queue.")
    async def showqueue(ctx):
        player = get_player(ctx.guild.id)

        if player.current_song is None and not player.queue:
            await ctx.send("The queue is empty.")
            return

        message = ""

        if player.current_song is not None:
            message += f"🎵 **Now playing:** {player.current_song.title}\n"

        if player.queue:
            message += "\n📋 **Queue:**\n"

            for index, song in enumerate(player.queue, start=1):
                message += f"`{index}.` {song.title}\n"

        await ctx.send(message)


    @bot.command(help="Skip the current song.")
    async def skip(ctx):
        player = get_player(ctx.guild.id)

        if (
            player.voice_client is None
            or player.current_song is None
            or (
                not player.voice_client.is_playing()
                and not player.paused
            )
        ):
            await ctx.send("Nothing is currently playing.")
            return

        skipped_song = player.current_song

        if player.paused:
            player.voice_client.resume()
            player.paused = False

        player.voice_client.stop()

        await asyncio.sleep(0.1)

        if player.current_song is not None and player.current_song != skipped_song:
            await ctx.send(
                f"⏭️ Skipped **{skipped_song.title}**.\n"
                f"▶️ Now playing **{player.current_song.title}**."
            )
        else:
            await ctx.send(
                f"⏭️ Skipped **{skipped_song.title}**.\n"
                f"📋 The queue is empty."
            )


    @bot.command(help="Pause the current song.")
    async def pause(ctx):
        player = get_player(ctx.guild.id)

        if player.voice_client is None or player.current_song is None:
            await ctx.send("Nothing is currently playing.")
            return

        if player.paused:
            await ctx.send("The music is already paused.")
            return

        if not player.voice_client.is_playing():
            await ctx.send("Nothing is currently playing.")
            return

        player.voice_client.pause()
        player.paused = True

        await ctx.send(
            f"⏸️ Paused **{player.current_song.title}**."
        )


    @bot.command(help="Resume the current song.")
    async def resume(ctx):
        player = get_player(ctx.guild.id)

        if player.voice_client is None or player.current_song is None:
            await ctx.send("Nothing is currently playing.")
            return

        if not player.paused:
            await ctx.send("The music isn't paused.")
            return

        player.voice_client.resume()
        player.paused = False

        await ctx.send(
            f"▶️ Resumed **{player.current_song.title}**."
        )


    @bot.command(help="Toggle current-song loop.")
    async def loop(ctx):
        player = get_player(ctx.guild.id)

        player.loop_enabled = not player.loop_enabled

        if player.loop_enabled:
            if player.loop_queue_enabled:
                await ctx.send(
                    "🔂 Current song loop enabled.\n"
                    "⚠️ Queue loop is still enabled, but current song loop takes priority."
                )
            else:
                await ctx.send("🔂 Current song loop enabled.")
        else:
            if player.loop_queue_enabled:
                await ctx.send(
                    "➡️ Current song loop disabled.\n"
                    "🔁 Queue loop is still enabled."
                )
            else:
                await ctx.send("➡️ Current song loop disabled.")


    @bot.command(help="Toggle queue loop.")
    async def loopqueue(ctx):
        player = get_player(ctx.guild.id)

        player.loop_queue_enabled = not player.loop_queue_enabled

        if player.loop_queue_enabled:
            if player.loop_enabled:
                await ctx.send(
                    "🔁 Queue loop enabled.\n"
                    "⚠️ Current song loop is enabled and takes priority."
                )
            else:
                await ctx.send("🔁 Queue loop enabled.")
        else:
            if player.loop_enabled:
                await ctx.send(
                    "➡️ Queue loop disabled.\n"
                    "🔂 Current song loop is still enabled."
                )
            else:
                await ctx.send("➡️ Queue loop disabled.")


    @bot.command(help="Clear the queue.")
    async def clear(ctx):
        player = get_player(ctx.guild.id)

        queue_count = len(player.queue)

        player.clear_queue()
        player.played_songs.clear()

        if queue_count == 0:
            await ctx.send("📋 The queue is already empty.")
            return

        await ctx.send(
            f"🗑️ Cleared **{queue_count}** song(s) from the queue."
        )


    @bot.command(help="Leave the voice channel.")
    async def leave(ctx):
        player = get_player(ctx.guild.id)

        if player.voice_client is None:
            await ctx.send("Klinoff is not in a voice channel.")
            return

        if player.voice_client.is_playing() or player.paused:
            player.voice_client.stop()

        player.clear_queue()
        player.played_songs.clear()
        player.current_song = None
        player.paused = False

        await player.voice_client.disconnect()
        player.voice_client = None

        await ctx.send("👋 Klinoff Left the voice channel.")


    @bot.command(help="Show the currently playing song.")
    async def nowplaying(ctx):
        player = get_player(ctx.guild.id)

        if player.current_song is None:
            await ctx.send("Nothing is currently playing.")
            return

        song = player.current_song

        if song.duration is not None:
            minutes, seconds = divmod(song.duration, 60)
            duration = f"{minutes}:{seconds:02d}"
        else:
            duration = "Unknown"

        if player.paused:
            status = "⏸️ Paused"
        else:
            status = "▶️ Playing"

        if player.loop_enabled and player.loop_queue_enabled:
            loop_status = "🔂 Current song (priority) + 🔁 Queue"
        elif player.loop_enabled:
            loop_status = "🔂 Current song"
        elif player.loop_queue_enabled:
            loop_status = "🔁 Queue"
        else:
            loop_status = "➡️ Off"

        await ctx.send(
            f"🎵 **{song.title}**\n"
            f"{status}\n"
            f"Duration: `{duration}`\n"
            f"Loop: {loop_status}\n"
            f"Queue: `{len(player.queue)}` song(s)"
        )


    @bot.command(help="Stop the queue.")
    async def stop(ctx):
        player = get_player(ctx.guild.id)

        player.loop_enabled = False
        player.loop_queue_enabled = False

        if player.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        if player.current_song is None and not player.queue:
            await ctx.send("Nothing is playing or queued.")
            return

        stopped_song = player.current_song

        if player.voice_client.is_playing() or player.paused:
            player.voice_client.stop()

        player.clear_queue()
        player.played_songs.clear()
        player.current_song = None
        player.paused = False

        if stopped_song is not None:
            await ctx.send(
                f"⏹️ Stopped **{stopped_song.title}** and cleared the queue."
            )
        else:
            await ctx.send("⏹️ Stopped playback and cleared the queue.")

    @bot.command(
        help="Delete recent messages.",
        hidden=True,
    )
    @commands.has_permissions(administrator=True)
    async def clearchat(ctx, amount: int = 1):
        if amount < 1:
            await ctx.send("❌ Amount must be at least `1`.")
            return

        if amount > 300:
            await ctx.send("❌ Amount cannot be greater than `300`.")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)

        await ctx.send(
            f"🧹 Deleted {len(deleted) - 1} message(s)."
        )

    @bot.command(help="Klinoff says...")
    async def sayd(ctx, *, message: str):
        await ctx.send(message)

    @bot.command(help="Show information about the bot.")
    async def info(ctx):
        await ctx.send(BOT_INFO)

    # error handling
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "❌ You don't have permission to use this command."
            )
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"❌ Missing required argument: `{error.param.name}`."
            )
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "❌ Invalid argument."
            )
            return

        print(f"Command error: {error}")
