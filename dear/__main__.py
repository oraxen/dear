# setup logger, all credits go to @Julien00859
import argparse
import logging

# cli options
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", action="count", help="increase verbosity", default=0
)
parser.add_argument(
    "-s", "--silent", action="count", help="decrease verbosity", default=0
)
parser.add_argument("--fps", action="store", type=int, default=60)
options = parser.parse_args()
verbosity = 10 * max(0, min(3 - options.verbose + options.silent, 5))

# logging configuration
stdout = logging.StreamHandler()
stdout.formatter = logging.Formatter(
    "{asctime} [{levelname}] <{name}:{funcName}> {message}", style="{"
)
logging.root.handlers.clear()
logging.root.addHandler(stdout)
logging.root.setLevel(verbosity)
logger = logging.getLogger(__name__)

import discord
import sys
from config import TomlConfig
from events import ReactionsListener

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects # all credits go to @agubelu
this = sys.modules[__name__]
this.running = False


def main():
    logger.info("starting up")
    config = TomlConfig("config.toml", "config.template.toml")
    client = discord.Client()

    @client.event
    async def on_ready():
        if this.running:
            return

        this.running = True

        activity = discord.Game(name=config.now_playing)
        await client.change_presence(status=discord.Status.online, activity=activity)

    ReactionsListener(config.ranks, client).load()
    client.run(config.token)


if __name__ == "__main__":
    main()
