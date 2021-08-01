from __future__ import annotations
from typing import (
    List, Any, Generator, Optional
)

import os
import fnmatch
import traceback
import logging

import asyncpg

import discord
from discord.ext import commands

import aiohttp

from utils.env import load_env


config = load_env("config/config.toml")
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter(r"%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger.addHandler(handler)


class Interbot(commands.Bot):
    """Welcome to interbot, your local do-it-all!"""

    def __init__(self, **kwargs) -> None:
        self.colour = kwargs.pop("colour", 0xfffffe)  # Colour used for all embeds, defaults to white
        self._prefix = kwargs.pop("prefix", self.get_pre)  # If a static prefix is given, else use callable

        super().__init__(command_prefix=self._prefix, **kwargs)

        self.cs: Optional[aiohttp.ClientSession] = None  # ClientSession for making API requests
        self.db: Optional[asyncpg.Pool] = None  # Database Pool

        self.loop.run_until_complete(self.session_init())

        self.load_from_folder(config.module_folder)  # Load extensions from the config's module folder
        self.load_extension("jishaku")  # Load jishaku for debug

    # Custom methods

    async def session_init(self) -> None:
        """Load all sessions such as database, ClientSession"""
        self.cs = aiohttp.ClientSession()  # Create the ClientSession
        self.db = await asyncpg.create_pool(**config.PG_CONFIG)  # Connect to the database using the config credentials

    @staticmethod
    async def get_pre(_: discord.Message, __: Interbot) -> str:
        """Get the bot prefix (may be updated at runtime)"""
        return config.prefix  # May be updated at runtime, so a callable prefix will also update

    @staticmethod
    def chunk(lst: List[Any], n: int) -> Generator[Any]:
        """Chunk a list into chunks of size n"""
        for i in range(0, len(lst), n):  # Iterate over the list in n intervals
            yield lst[i:i + n]  # Yield all items between now and next interval

    def load_from_folder(self, directory: str, *, ignore_suffix: str = "__", remove_char_amount: int = 3) -> None:
        """Load cogs from a certain folder"""
        results = []

        for base, dirs, files in os.walk(directory):
            goodfiles = fnmatch.filter(files, "*.py")  # Filter out non-python files

            results.extend(
                os.path.join(base, f).replace("\\", ".")[:-remove_char_amount] for f in goodfiles
                if not f.startswith(ignore_suffix)
            )  # Extend the results in a loadable format, omitting ignored files

        for ext in results:
            try:
                self.load_extension(ext)  # Load the extension
                logger.info(f"[Cog Load] {ext} loaded successfully")  # Log the load
            except commands.ExtensionError as _:
                traceback.print_exc()  # If the load failed, output the traceback

    # Gateway events

    async def on_ready(self) -> None:
        """READY gateway event"""
        print(f"{self.user} connected and ready.")  # Printed upon READY event firing


bot = Interbot()

if __name__ == '__main__':
    bot.run(config.token)
