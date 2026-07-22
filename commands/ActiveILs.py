import interactions
import database.categories
import database.Maps
from UI import ILsheet


class ILMapCategories(interactions.Extension):
    @interactions.slash_command(
        name="activeils",
        description="Show which il categories are currently active and contributing to IL points"
    )

    async def ilmapcats(self, ctx: interactions.SlashContext):
        categories = database.categories.getMainILCategories(self.bot.db)

        map_rows = database.Maps.getMainLevels(self.bot.db, includeAdvanced=True)

        headers = ["Map"] + [category.name[0].upper() for category in categories]

        map_column = [[map_obj.name] for map_obj in map_rows]
        category_columns = []

        for category in categories:
            statuses = []
            for map_obj in map_rows:
                active = database.categories.checkILActiveness(self.bot.db, map_obj.id, category.id)
                statuses.append(["O" if active else "-"])
            category_columns.append(statuses)

        columns = [map_column] + category_columns
        table = ILsheet.generateSheet(headers, columns)

        await ctx.send("Active IL Categories\n```\n" + table + "```")
