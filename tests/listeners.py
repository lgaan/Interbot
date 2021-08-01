import traceback
import sys
from typing import Optional

import discord
from discord.ext import commands

from main import Interbot


class Listeners(commands.Cog, command_attrs={"hidden": True}):
    """Listeners go here"""

    def __init__(self, bot: Interbot) -> None:
        self.bot = bot

        self.bot.check(self.check_role_locks)

        self.no_log = (commands.CommandNotFound,)

    async def check_role_locks(self, ctx: commands.Context) -> Optional[bool]:
        """Check for role locked commands"""
        lock = await self.bot.db.fetchrow(
            "SELECT * FROM role_lock WHERE gid=$1 AND command=$2",
            ctx.guild.id, ctx.command.name
        )

        if lock:
            await commands.has_any_role(*lock["roles"]).predicate(ctx)

        return True

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> Optional[discord.Message]:
        """Listener to catch all command errors"""
        error = getattr(error, "original", error)  # For CommandInvokeErrors
        error_message = str(error)

        if isinstance(error, self.no_log):  # The error is a type we want to ignore
            return

        elif isinstance(error, commands.MissingAnyRole):
            roles = [ctx.guild.get_role(role).mention for role in error.missing_roles]  # Convert each role to a mention

            error_message = f"You need at least one of the following roles to run this command!\n{', '.join(roles)}"
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        embed = discord.Embed(
            description=error_message,
            colour=self.bot.colour
        )
        embed.set_author(icon_url=ctx.author.avatar.url, name=f"An error occurred!")
        embed.set_footer(icon_url=ctx.me.avatar.url, text=ctx.me.display_name)

        return await ctx.reply(
            embed=embed,
            mention_author=False
        )


def setup(bot: Interbot):
    bot.add_cog(Listeners(bot))
