import ssl
import irc.bot
import irc.connection
import re
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
from jaraco.stream import buffer
import time
from bs4 import BeautifulSoup

class GhostBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, server, port=6697):
        irc.client.ServerConnection.buffer_class = buffer.LenientDecodingLineBuffer
        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname, connect_factory=factory)
        self.channels = channels

    def on_welcome(self, c, e):
        for channel in self.channels:
            c.join(channel)
            self.channels[channel] = irc.bot.Channel()

    def on_pubmsg(self, c, e):
        channel = e.target
        messages = e.arguments[0]
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', messages)
        for url in urls:
            try:
                resp = self.robust_request(url)
                if resp:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    title = soup.title.text if soup.title else 'No title found'
                    if title != 'No title found':
                        self.send_custom_youtube_message(c, channel, title)
            except Exception as exc:
                print(f"Failed to fetch title for {url}: {exc}")

    def send_custom_youtube_message(self, c, channel, message):
        message = message.replace('\r', ' ').replace('\n', ' ')
        if 'youtube' in message.lower() or 'youtu.be' in message.lower():
            message_parts = re.split('(YouTube)', message, flags=re.IGNORECASE)
            new_message = ''
            for part in message_parts:
                if part.lower() == 'youtube':
                    new_message += '\x0304,00' + 'You' + '\x0300,04' + 'Tube' + '\x03'
                else:
                    new_message += part
            c.privmsg(channel, new_message)
        else:
            c.privmsg(channel, message)

    def robust_request(self, url):
        retries = 3
        backoff_factor = 2
        delay = 1
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                return response
            except HTTPError as http_err:
                if response.status_code == 403:
                    print(f"Attempt {attempt + 1} failed: {response.status_code} Forbidden for url: {url}")
                    break
                elif response.status_code == 429:
                    print(f"Attempt {attempt + 1} failed: {response.status_code} Too Many Requests for url: {url}")
                    time.sleep(delay)
                    delay *= backoff_factor
                else:
                    print(f"Attempt {attempt + 1} failed: {http_err}")
                    time.sleep(delay)
                    delay *= backoff_factor
            except (ConnectionError, Timeout) as err:
                print(f"Attempt {attempt + 1} failed: {err}")
                time.sleep(delay)
                delay *= backoff_factor
        return None

    def on_disconnect(self, c, e):
        time.sleep(5)
        self.jump_server()

def main():
    server = "irc.twistednet.org"
    channels = {"#Twisted": None, "#g6": None}
    nickname = "u"

    bot = GhostBot(channels, nickname, server)
    while True:
        try:
            bot.start()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
