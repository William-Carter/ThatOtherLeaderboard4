import interactions

class testCommand(interactions.Extension):
    @interactions.slash_command(
            name="my_command", 
            description="My first command :(", 
            scopes=[1081155162065862697])

    async def my_command_function(self, ctx: interactions.SlashContext):
        await ctx.send("Hello World")