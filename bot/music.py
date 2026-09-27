import asyncio, yt_dlp, discord
from dataclasses import dataclass

YTDLP_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
}

"""
song dataclass:
song.title: str
song.webpage_url: str
song.duration: int or None
song.stream_url: str or None
"""
@dataclass
class Song:
    title: str
    webpage_url: str
    duration: int | None
    stream_url: str | None = None


class MusicPlayer:
    def __init__(self):
        self.queue = []
        self.played_songs = []
        self.current_song = None
        self.loop_enabled = False
        self.loop_queue_enabled = False
        self.paused = False
        self.voice_client = None

    def add_to_queue(self, song: Song):
        self.queue.append(song)

    def get_next_song(self) -> Song | None:
        if not self.queue:
            return None

        return self.queue.pop(0)

    def clear_queue(self):
        self.queue.clear()

    def enable_loop(self):
        self.loop_enabled = True

    def disable_loop(self):
        self.loop_enabled = False

    def enable_loop_queue(self):
        self.loop_queue_enabled = True

    def disable_loop_queue(self):
        self.loop_queue_enabled = False


players = {}


def get_player(guild_id):
    if guild_id not in players:
        players[guild_id] = MusicPlayer()

    return players[guild_id]

def extract_song(query: str) -> Song | None:
    with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
        try:
            if query.startswith(("http://", "https://")):
                info = ydl.extract_info(query, download=False)
            else:
                info = ydl.extract_info(
                    f"ytsearch1:{query}",
                    download=False,
                )

                if not info or not info.get("entries"):
                    return None

                info = info["entries"][0]

            if not info:
                return None

            return Song(
                title=info.get("title", "Unknown title"),
                webpage_url=info.get("webpage_url", query),
                duration=info.get("duration"),
                stream_url=info.get("url"),
            )

        except yt_dlp.utils.DownloadError:
            return None

def get_stream_url(song: Song) -> str | None:
    options = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            info = ydl.extract_info(song.webpage_url, download=False)

            if not info:
                return None

            return info.get("url")

        except yt_dlp.utils.DownloadError:
            return None

async def play_song(player: MusicPlayer, bot, song: Song | None = None) -> bool:
    if player.voice_client is None:
        return False

    if song is None:
        song = player.get_next_song()

    if song is None:
        if player.loop_queue_enabled and player.played_songs:
            player.queue.extend(player.played_songs)
            player.played_songs.clear()

            song = player.get_next_song()
        else:
            player.current_song = None
            return False

    stream_url = get_stream_url(song)

    if stream_url is None:
        return False

    player.current_song = song
    player.paused = False

    ffmpeg_options = {
        "before_options": (
            "-reconnect 1 "
            "-reconnect_streamed 1 "
            "-reconnect_delay_max 5"
        ),
        "options": "-vn",
    }

    source = discord.FFmpegOpusAudio(
        stream_url,
        **ffmpeg_options,
    )

    def after_playback(error):
        if error:
            print(f"Playback error: {error}")

        if player.loop_enabled:
            next_song = player.current_song
        else:
            if player.loop_queue_enabled and player.current_song is not None:
                player.played_songs.append(player.current_song)

            next_song = None

        bot.loop.call_soon_threadsafe(
            asyncio.create_task,
            play_song(player, bot, next_song),
        )

    player.voice_client.play(
        source,
        after=after_playback,
    )

    return True


if __name__ == "__main__":
    player = MusicPlayer()

    player.add_to_queue({"title": "Test Song"})
    player.add_to_queue({"title": "Another Song"})

    print(player.queue)
    print(player.get_next_song())
    print(player.queue)

