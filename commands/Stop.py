import interactions
import tol
import sys

class Stop(interactions.Extension):
    @interactions.slash_command(
        name="stop",
        description="Stop the bot",
        scopes=[tol.homeGuild]
    )

    async def stop(self, ctx: interactions.SlashContext):
        await ctx.send("Stopping!")
        sys.exit()
            

