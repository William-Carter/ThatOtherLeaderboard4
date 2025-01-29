import interactions
import UI.durations
import database.leaderboards
import database.sprm
from database.models import Category
class Records(interactions.Extension):
    @interactions.slash_command(
        name="records",
        description="See the records for categories",
    )

    @interactions.slash_option(
        name="country",
        argument_name="country",
        description="Which country to see the records for",
        required=False,
        opt_type=interactions.OptionType.STRING
    )

    @interactions.slash_option(
        name="continent",
        argument_name="continent",
        description="Which continent to see the records for",
        required=False,
        opt_type=interactions.OptionType.STRING
    )  

    @interactions.slash_option(
        name="include-extensions",
        argument_name="extensions",
        description="Whether to include category extensions",
        required=False,
        opt_type=interactions.OptionType.BOOLEAN
    )
    
    
    async def records(self, ctx: interactions.SlashContext, country: str, continent: str, extensions: bool):
        pass