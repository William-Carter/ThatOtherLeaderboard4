import interactions
import tol

class Trust(interactions.Extension):
    @interactions.slash_command(
        name="trust",
        description="Trust a user",
        scopes=[1081155162065862697]
    )

    @interactions.slash_option(
        name="user",
        argument_name="user",
        description="The user you want to trust",
        required=True,
        opt_type=interactions.OptionType.USER
    )

    async def trust(self, ctx: interactions.SlashContext, user: interactions.User):
        memberInstances = user.member_instances
        member = None

        for instance in memberInstances:
            if instance.guild.id == tol.homeGuild:
                member = instance
                break

        if not member:
            await ctx.send("User not in TOL server!")
            return

        if member.has_role(tol.trustedRole):
            await member.remove_role(tol.trustedRole)
            await ctx.send(f"Untrusted {user.display_name}!")

        else:
            await   member.add_role(tol.trustedRole)
            await ctx.send(f"Trusted {user.display_name}!")
        
            

