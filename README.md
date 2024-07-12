# IRC URL Headline Bot

IRC URL Headline Bot is an IRC bot designed to enhance your IRC channel experience by fetching webpage titles, specifically for YouTube links, and handling various connection and messaging functionalities.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
  - [Welcome and Join Channels](#welcome-and-join-channels)
  - [Message Handling](#message-handling)
  - [YouTube Link Formatting](#youtube-link-formatting)
  - [Robust URL Request Handling](#robust-url-request-handling)
  - [Automatic Reconnection](#automatic-reconnection)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

IRC URL Headline Bot is a robust and feature-rich IRC bot written in Python. It automatically joins specified channels, processes messages to fetch webpage titles, and applies custom formatting for YouTube links.

## Features

### Welcome and Join Channels

- Automatically joins a list of predefined channels upon connection.
- Initializes a channel object for each joined channel.

### Message Handling

- Parses messages for URLs.
- Fetches the title of the webpage if a URL is detected.
- Handles exceptions during the fetching process gracefully.

### YouTube Link Formatting

- Customizes messages containing YouTube links by applying different color codes to the word "YouTube".

### Robust URL Request Handling

- Implements robust URL fetching with retries and exponential backoff.
- Handles HTTP errors, connection errors, and timeouts.

### Automatic Reconnection

- Automatically attempts to reconnect after disconnection with a delay.

## Installation

To install IRC URL Headline Bot, ensure you have Python3 and the required libraries:

```bash
pip3 install irc requests jaraco.stream beautifulsoup4
```

## Usage

Run the bot using the following command:

```bash
python3 IRCURLHeadlineBot.py
```

## Configuration

Edit the `main` function in `IRCURLHeadlineBot.py` to configure the server, channels, and nickname:

```python
def main():
    server = "irc.twistednet.org"
    channels = {"#Twisted": None, "#g6": None}
    nickname = "u"
```

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
