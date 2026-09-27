from discord.ext import commands


class MusicHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        message = "**Klinoff Music — Help**\n\n"

        for cog, commands_list in mapping.items():
            if not commands_list:
                continue

            for command in commands_list:
                if command.hidden:
                    continue

                if any(
                    getattr(check, "perms", {}).get("administrator") is True
                    for check in command.checks
                ):
                    continue

                message += (
                    f"`!{command.name}` — "
                    f"{command.help or 'No description available.'}\n"
                )

        await self.get_destination().send(message)
