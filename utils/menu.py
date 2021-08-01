from typing import List

import discord
from discord.ext import commands

from discord.ext import menus
from discord.ext.menus.views import ViewMenu


class EmbedMenu(ViewMenu):
    def __init__(self, embeds: List[discord.Embed], *args, **kwargs) -> None:
        self.embeds = embeds

        self.page = self.embeds[0]
        self.page_number = 0

        super().__init__(*args, **kwargs)

    async def send_initial_message(self, ctx: commands.Context, channel: discord.abc.Messageable) -> discord.Message:
        return await self.send_with_view(channel, embed=self.embeds[0])

    @menus.button("\U000025c0")
    async def on_arrow_back(self, _: discord.Interaction) -> discord.Message:
        self.page_number = self.page_number - 1

        if self.page_number < 0:
            self.page_number = 0

        self.page = self.embeds[self.page_number]

        return await self.message.edit(embed=self.page)

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def on_stop(self, _) -> None:
        self.stop()

    @menus.button("\U000025b6")
    async def on_arrow_forward(self, _: discord.Interaction) -> discord.Message:
        self.page_number = self.page_number + 1

        if self.page_number > len(self.embeds) - 1:
            self.page_number = len(self.embeds)

        self.page = self.embeds[self.page_number]

        return await self.message.edit(embed=self.page)
