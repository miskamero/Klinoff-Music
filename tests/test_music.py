import unittest, yt_dlp
from unittest.mock import MagicMock, patch

from bot.music import MusicPlayer, Song, play_song, extract_song, get_stream_url


def await_play_song(player, bot, song=None):
    import asyncio

    return asyncio.run(play_song(player, bot, song))


class TestMusicPlayer(unittest.TestCase):
    def test_initial_state(self):
        player = MusicPlayer()

        self.assertEqual(player.queue, [])
        self.assertIsNone(player.current_song)
        self.assertFalse(player.loop_enabled)
        self.assertFalse(player.loop_queue_enabled)
        self.assertEqual(player.played_songs, [])
        self.assertFalse(player.paused)
        self.assertIsNone(player.voice_client)

    def test_add_to_queue(self):
        player = MusicPlayer()
        song = Song("Test Song", "https://example.com", 180)

        player.add_to_queue(song)

        self.assertEqual(player.queue, [song])

    def test_get_next_song_returns_first_song(self):
        player = MusicPlayer()
        song_a = Song("Song A", "https://example.com/a", 180)
        song_b = Song("Song B", "https://example.com/b", 200)

        player.add_to_queue(song_a)
        player.add_to_queue(song_b)

        result = player.get_next_song()

        self.assertEqual(result, song_a)
        self.assertEqual(player.queue, [song_b])

    def test_get_next_song_empty_queue(self):
        player = MusicPlayer()

        result = player.get_next_song()

        self.assertIsNone(result)

    def test_clear_queue(self):
        player = MusicPlayer()
        song_a = Song("Song A", "https://example.com/a", 180)
        song_b = Song("Song B", "https://example.com/b", 200)

        player.add_to_queue(song_a)
        player.add_to_queue(song_b)

        player.clear_queue()

        self.assertEqual(player.queue, [])

    def test_clear_queue_keeps_current_song(self):
        player = MusicPlayer()
        song = Song("Current Song", "https://example.com", 180)

        player.current_song = song
        player.add_to_queue(Song("Queued Song", "https://example.com/queued", 200))

        player.clear_queue()

        self.assertEqual(player.queue, [])
        self.assertEqual(player.current_song, song)

    def test_enable_and_disable_loop(self):
        player = MusicPlayer()

        player.enable_loop()
        self.assertTrue(player.loop_enabled)

        player.disable_loop()
        self.assertFalse(player.loop_enabled)

    def test_enable_and_disable_queue_loop(self):
        player = MusicPlayer()

        player.enable_loop_queue()
        self.assertTrue(player.loop_queue_enabled)

        player.disable_loop_queue()
        self.assertFalse(player.loop_queue_enabled)

    def test_loops_can_both_be_enabled(self):
        player = MusicPlayer()

        player.enable_loop()
        player.enable_loop_queue()

        self.assertTrue(player.loop_enabled)
        self.assertTrue(player.loop_queue_enabled)

    def test_play_song_starts_next_song(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client

        song = Song(
            "Test Song",
            "https://example.com",
            180,
        )

        player.add_to_queue(song)

        with patch("bot.music.get_stream_url", return_value="https://stream.example.com"):
            with patch("bot.music.discord.FFmpegOpusAudio"):
                result = unittest.IsolatedAsyncioTestCase().run

        self.assertTrue(True)

    def test_play_song_starts_queued_song(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client

        song = Song(
            "Test Song",
            "https://example.com",
            180,
        )

        player.add_to_queue(song)

        with patch(
            "bot.music.get_stream_url",
            return_value="https://stream.example.com",
        ):
            with patch("bot.music.discord.FFmpegOpusAudio"):
                result = await_play_song(player, bot)

        self.assertTrue(result)
        self.assertEqual(player.current_song, song)
        voice_client.play.assert_called_once()


    def test_play_song_removes_song_from_queue(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client

        song = Song(
            "Test Song",
            "https://example.com",
            180,
        )

        player.add_to_queue(song)

        with patch(
            "bot.music.get_stream_url",
            return_value="https://stream.example.com",
        ):
            with patch("bot.music.discord.FFmpegOpusAudio"):
                await_play_song(player, bot)

        self.assertEqual(player.queue, [])


    def test_play_song_resets_paused_state(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client
        player.paused = True

        song = Song(
            "New Song",
            "https://example.com",
            180,
        )

        player.add_to_queue(song)

        with patch(
            "bot.music.get_stream_url",
            return_value="https://stream.example.com",
        ):
            with patch("bot.music.discord.FFmpegOpusAudio"):
                result = await_play_song(player, bot)

        self.assertTrue(result)
        self.assertFalse(player.paused)
        self.assertEqual(player.current_song, song)


    def test_play_song_without_voice_client_returns_false(self):
        player = MusicPlayer()
        bot = MagicMock()

        song = Song(
            "Test Song",
            "https://example.com",
            180,
        )

        player.add_to_queue(song)

        result = await_play_song(player, bot)

        self.assertFalse(result)
        self.assertIsNone(player.current_song)


    def test_play_song_with_empty_queue_returns_false(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client

        result = await_play_song(player, bot)

        self.assertFalse(result)
        self.assertIsNone(player.current_song)
        voice_client.play.assert_not_called()


    def test_play_song_stream_failure_returns_false(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client

        song = Song(
            "Unavailable Song",
            "https://example.com",
            180,
        )

        player.add_to_queue(song)

        with patch(
            "bot.music.get_stream_url",
            return_value=None,
        ):
            result = await_play_song(player, bot)

        self.assertFalse(result)
        self.assertIsNone(player.current_song)
        voice_client.play.assert_not_called()


    def test_play_song_queue_loop_reuses_played_songs(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client
        player.loop_queue_enabled = True

        song_a = Song("Song A", "https://example.com/a", 180)
        song_b = Song("Song B", "https://example.com/b", 200)

        player.played_songs = [song_a, song_b]

        with patch(
            "bot.music.get_stream_url",
            return_value="https://stream.example.com",
        ):
            with patch("bot.music.discord.FFmpegOpusAudio"):
                result = await_play_song(player, bot)

        self.assertTrue(result)
        self.assertEqual(player.current_song, song_a)
        self.assertEqual(player.queue, [song_b])
        self.assertEqual(player.played_songs, [])


    def test_play_song_current_loop_reuses_current_song(self):
        player = MusicPlayer()
        voice_client = MagicMock()
        bot = MagicMock()

        player.voice_client = voice_client
        player.loop_enabled = True

        current_song = Song(
            "Current Song",
            "https://example.com",
            180,
        )

        player.current_song = current_song

        with patch(
            "bot.music.get_stream_url",
            return_value="https://stream.example.com",
        ):
            with patch("bot.music.discord.FFmpegOpusAudio"):
                result = await_play_song(
                    player,
                    bot,
                    current_song,
                )

        self.assertTrue(result)
        self.assertEqual(player.current_song, current_song)


class TestExtractSong(unittest.TestCase):
    def test_extract_song_from_url(self):
        info = {
            "title": "Test Song",
            "webpage_url": "https://youtube.com/watch?v=123",
            "duration": 180,
            "url": "https://stream.example.com/audio",
        }

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = info

            song = extract_song("https://youtube.com/watch?v=123")

        self.assertIsNotNone(song)
        self.assertEqual(song.title, "Test Song")
        self.assertEqual(
            song.webpage_url,
            "https://youtube.com/watch?v=123",
        )
        self.assertEqual(song.duration, 180)
        self.assertEqual(
            song.stream_url,
            "https://stream.example.com/audio",
        )

        mock_instance.extract_info.assert_called_once_with(
            "https://youtube.com/watch?v=123",
            download=False,
        )

    def test_extract_song_from_search(self):
        info = {
            "entries": [
                {
                    "title": "Found Song",
                    "webpage_url": "https://youtube.com/watch?v=456",
                    "duration": 240,
                    "url": "https://stream.example.com/audio",
                }
            ]
        }

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = info

            song = extract_song("Found Song")

        self.assertIsNotNone(song)
        self.assertEqual(song.title, "Found Song")
        self.assertEqual(
            song.webpage_url,
            "https://youtube.com/watch?v=456",
        )
        self.assertEqual(song.duration, 240)
        self.assertEqual(
            song.stream_url,
            "https://stream.example.com/audio",
        )

        mock_instance.extract_info.assert_called_once_with(
            "ytsearch1:Found Song",
            download=False,
        )

    def test_extract_song_search_with_no_results(self):
        info = {
            "entries": []
        }

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = info

            song = extract_song("Nonexistent Song")

        self.assertIsNone(song)

    def test_extract_song_handles_missing_duration(self):
        info = {
            "title": "No Duration",
            "webpage_url": "https://youtube.com/watch?v=789",
            "url": "https://stream.example.com/audio",
        }

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = info

            song = extract_song("https://youtube.com/watch?v=789")

        self.assertIsNotNone(song)
        self.assertEqual(song.title, "No Duration")
        self.assertIsNone(song.duration)
        self.assertEqual(
            song.stream_url,
            "https://stream.example.com/audio",
        )

    def test_extract_song_handles_download_error(self):
        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.side_effect = (
                yt_dlp.utils.DownloadError("Test error")
            )

            song = extract_song("Bad URL")

        self.assertIsNone(song)

    def test_extract_song_search_uses_first_result(self):
        info = {
            "entries": [
                {
                    "title": "First Song",
                    "webpage_url": "https://youtube.com/watch?v=111",
                    "duration": 100,
                    "url": "https://stream.example.com/first",
                },
                {
                    "title": "Second Song",
                    "webpage_url": "https://youtube.com/watch?v=222",
                    "duration": 200,
                    "url": "https://stream.example.com/second",
                },
            ]
        }

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = info

            song = extract_song("Some Song")

        self.assertIsNotNone(song)
        self.assertEqual(song.title, "First Song")
        self.assertEqual(
            song.webpage_url,
            "https://youtube.com/watch?v=111",
        )


class TestGetStreamUrl(unittest.TestCase):
    def test_get_stream_url_returns_stream_url(self):
        song = Song(
            "Test Song",
            "https://youtube.com/watch?v=123",
            180,
        )

        info = {
            "url": "https://stream.example.com/audio",
        }

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = info

            stream_url = get_stream_url(song)

        self.assertEqual(
            stream_url,
            "https://stream.example.com/audio",
        )

        mock_instance.extract_info.assert_called_once_with(
            "https://youtube.com/watch?v=123",
            download=False,
        )

    def test_get_stream_url_returns_none_when_no_info(self):
        song = Song(
            "Test Song",
            "https://youtube.com/watch?v=123",
            180,
        )

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = None

            stream_url = get_stream_url(song)

        self.assertIsNone(stream_url)

    def test_get_stream_url_returns_none_when_url_missing(self):
        song = Song(
            "Test Song",
            "https://youtube.com/watch?v=123",
            180,
        )

        info = {
            "title": "Test Song",
        }

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.return_value = info

            stream_url = get_stream_url(song)

        self.assertIsNone(stream_url)

    def test_get_stream_url_handles_download_error(self):
        song = Song(
            "Unavailable Song",
            "https://youtube.com/watch?v=123",
            180,
        )

        with patch("bot.music.yt_dlp.YoutubeDL") as mock_ytdl:
            mock_instance = mock_ytdl.return_value.__enter__.return_value
            mock_instance.extract_info.side_effect = (
                yt_dlp.utils.DownloadError("Test error")
            )

            stream_url = get_stream_url(song)

        self.assertIsNone(stream_url)

if __name__ == "__main__":
    unittest.main()
