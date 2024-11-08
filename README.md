# Discord Music Bot

This is a Discord music bot that can play music from YouTube, manage a queue, and provide various music-related commands.

## Sections

- [Features](#features)
- [Requirements](#requirements)
- [Commands](#commands)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- Play music from YouTube using URLs or search queries
- Manage a queue of songs
- Pause, resume, skip, and stop songs
- Loop the current song
- Show the current queue
- Clear the queue
- Join and leave voice channels
- Clear chat messages

## Requirements

- Python 3.8 or higher
- [discord.py](https://pypi.org/project/discord.py/)
- [yt-dlp](https://pypi.org/project/youtube-dl/)

**Note:** The dependencies can be installed using the following command:
```sh
pip install -r requirements.txt
```

## Commands

- `!hi` - Responds with "Hello!"
- `!ping` - Shows the bot's latency
- `!sayd [message]` - Repeats the given message
- `!play [url or search query]` - Plays a song from YouTube
- `!pause` - Pauses or resumes the current song
- `!skip` - Skips the current song
- `!stop` - Stops the bot and disconnects from the voice channel
- `!loop` - Loops the current song
- `!showqueue` - Shows the current queue
- `!clear` - Clears the queue and stops the current song
- `!leave` - Disconnects the bot from the voice channel
- `!clearchat [amount]` - Clears the specified number of chat messages

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/discord-music-bot.git
    ```
2. Navigate to the project directory:
    ```sh
    cd discord-music-bot
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Add your bot token to `token.txt`.

## Usage

Run the bot:
```sh
python [main.py](http://_vscodecontentref_/1)