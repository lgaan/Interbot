from discord.ext import commands


class CommandConverter(commands.Converter):
    """Convert a string into a command object"""

    async def convert(self, ctx: commands.Context, argument: str) -> commands.Command:
        """Convert the argument"""
        command = ctx.bot.get_command(argument)

        if not command:
            raise commands.BadArgument(f"Command with name {argument} not found.")

        return command
