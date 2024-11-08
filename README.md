# Klinoff Music

Klinoff Music is a multipurpose Discord Bot that allows users in your server to play music from YouTube using URLs or search queries. While the main purpose of the bot is to play music, it also has some other features for easy management of messages!

## Sections

- [Features](#features)
- [Requirements](#requirements)
- [Commands](#commands)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](LICENSE)

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
- `!pause` - Pauses or unpauses the current song
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
    git clone https://github.com/miskamero/Klinoff-Music.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Klinoff-Music
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Add your bot token from the [Discord Developer Portal](https://discord.com/developers/applications) to the `token.txt` file:
    ```sh
    echo "YOUR_BOT_TOKEN" > token.txt
    ```
5. Run the bot:
    ```sh
    python main.py
    ```


## Contributing

Contributions are always welcome! If you have any suggestions or improvements, please create an issue or pull request.

### Pull Requests

Make sure you have installed the dependencies and the appropriate Python version.

1. Fork the repository.
2. Create a new branch with a descriptive name:
    ```sh
    git checkout -b feature/my-feature
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m "Add my feature"
    ```
4. Push your branch to your fork:
    ```sh
    git push origin feature/my-feature
    ```
5. Create a pull request from your branch to the `main` branch of the original repository.

## Known Issues

Perfect app, No Issues!