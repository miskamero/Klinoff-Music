# Klinoff Music

Your next favorite Discord music bot built with Python and discord.py; a powerful tool for enhancing your Discord experience. **Klinoff Music** allows users to play music from YouTube using URLs or search queries, manage a song queue, control playback, and use several utility commands for server management.

## Features

- Play YouTube videos using URLs or search queries
- Automatic voice-channel joining when starting playback
- Song queue management
- Pause and resume playback
- Skip songs
- Stop playback and clear the queue
- Current-song and queue looping
- View the current queue
- View the currently playing song
- Leave the voice channel
- Delete recent chat messages
- Custom help command
- 28 automated unit tests for the music-player and YouTube extraction logic

## Commands

### Music

| Command | Description |
|---|---|
| `!play <URL or search>` | Add and play a YouTube song |
| `!pause` | Pause the current song |
| `!resume` | Resume the paused song |
| `!skip` | Skip the current song |
| `!stop` | Stop playback and clear the queue |
| `!loop` | Toggle current-song looping |
| `!loopqueue` | Toggle queue looping |
| `!showqueue` | Show the current queue |
| `!nowplaying` | Show information about the current song |
| `!clear` | Clear the queued songs |
| `!leave` | Leave the voice channel and reset playback state |

### Utility

| Command | Description |
|---|---|
| `!ping` | Show the bot's latency |
| `!hi` | Respond with "Oink!" |
| `!sayd <message>` | Make the bot send a message |
| `!info` | Show information about the bot |

### Administrator commands

These commands are intentionally hidden from the help command.

| Command | Description |
|---|---|
| `!join` | Join or move to the administrator's voice channel |
| `!clearchat [amount]` | Delete recent messages |

`!clearchat` accepts between 1 and 300 messages. The command itself is not shown in `!help`.

## Requirements

- Python 3.8+
- FFmpeg
- A Discord bot application
- The Python dependencies listed in `requirements.txt`

Python dependencies:

- [discord.py](https://pypi.org/project/discord.py/)
- [yt-dlp](https://pypi.org/project/yt-dlp/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [PyNaCl](https://pypi.org/project/PyNaCl/)
- [davey](https://pypi.org/project/davey/)

Install the dependencies with:

```sh
pip install -r requirements.txt
```

## Installation

1. Clone the repository

```sh
git clone https://github.com/miskamero/Klinoff-Music.git
cd Klinoff-Music
```
2. Create a virtual environment (optional but recommended)§

3. Install dependencies

```sh
pip install -r requirements.txt
```

4. Configure the bot token

Create a .env file in the project root and add your Discord bot token like this:

`DISCORD_TOKEN=YOUR_BOT_TOKEN`

Create your Discord bot application through the [Discord Developer Portal](https://discord.com/developers/applications) and copy its bot token into .env.

The bot also requires the appropriate Discord permissions and intents, including the Message Content Intent.

5. Install FFmpeg

FFmpeg is required for audio playback.

Make sure the ffmpeg executable is available in your system's PATH.

6. Run the bot
```sh
python main.py
```

## Testing

The project contains unit tests for the music-player logic and YouTube extraction.

Run all tests with:

```sh
python -m unittest tests.test_music -v
```

The current test suite contains 28 tests covering:

Queue management
Song selection
Playback state
Pause state handling
Current-song looping
Queue looping
Stream extraction
YouTube URL extraction
YouTube search
yt-dlp error handling

## Project Structure

```text
Klinoff-Music/
├── bot/
│   ├── __init__.py
│   ├── commands.py
│   ├── help.py
│   ├── info.py
│   └── music.py
├── tests/
│   └── test_music.py
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Main components


`main.py` — Bot initialization and startup
`bot/commands.py` — Discord commands and command error handling
`bot/music.py` — Music player, queue, YouTube extraction, and playback logic
`bot/help.py` — Custom help command
`bot/info.py` — Bot information
`tests/test_music.py` — Unit tests for music functionality

## Contributing

Contributions are welcome!

To contribute:

1. Fork the repository.

2. Create a new branch:
   ```sh
   git checkout -b feature/my-feature
   ```
3. Make your changes.

4. Run the test suite:
   ```sh
   python -m unittest tests.test_music -v
   ```

5. Commit your changes:
   ```sh
   git commit -m "Add my feature"
   ```
6. Push your branch:
   ```sh
   git push origin feature/my-feature
   ```
7. Open a pull request.

## License

Klinoff Music is licensed under the GNU General Public License v3.0.
See the [LICENSE](LICENSE) file for the full license text.

## Known Issues

Perfect app, No Issues!
