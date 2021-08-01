from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from main import Interbot
from utils.converters import CommandConverter
from utils.menu import EmbedMenu


if TYPE_CHECKING:
    CommandConverter = commands.Command


class Configuration(commands.Cog):
    def __init__(self, bot: Interbot) -> None:
        self.bot = bot

    @commands.group(name="config", invoke_without_subcommand=True)
    @commands.has_permissions(manage_guild=True)
    async def config_(self, ctx: commands.Context) -> discord.Message:
        """Configure guild settings (role locked commands, etc)"""
        role_locks = await self.bot.db.fetch("SELECT * FROM role_lock WHERE gid=$1", ctx.guild.id)

        embeds = []

        for entry in self.bot.chunk(role_locks, 1):
            desc = ""

            for item in entry:
                desc += f"\n{item['command']} -> {', '.join([ctx.guild.get_role(r).mention for r in item['roles']])}"

            embed = discord.Embed(
                description=desc,
                colour=self.bot.colour
            )

            embed.set_author(icon_url=ctx.author.avatar.url, name=f"{ctx.guild}'s role locked commands")
            embed.set_footer(icon_url=ctx.me.avatar.url, text=ctx.me.display_name)

            embeds.append(embed)

        menu = EmbedMenu(embeds, clear_reactions_after=True)
        return await menu.start(ctx)

    @config_.command(name="role-lock", aliases=["rl"])
    async def role_lock_(
        self,
        ctx: commands.Context,
        roles: commands.Greedy[discord.Role],
        *, command: CommandConverter
    ) -> discord.Message:
        """Set a command to only work with certain roles"""
        roles = [role.id for role in roles]

        await self.bot.db.execute("DELETE FROM role_lock WHERE gid=$1 AND command=$2", ctx.guild.id, command.name)
        await self.bot.db.execute(
            "INSERT INTO role_lock (gid, command, roles) VALUES ($1, $2, $3)",
            ctx.guild.id, command.name, roles
        )

        return await ctx.reply(
            f"Command {command} has been role locked to `{len(roles)}` role(s) successfully.",
            mention_author=False
        )


def setup(bot: Interbot):
    bot.add_cog(Configuration(bot))
