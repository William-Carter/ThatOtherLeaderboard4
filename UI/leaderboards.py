import UI.neatTables

class Leaderboard():
    def __init__(self, columnNames: list[str], data: list[list[any]], keyColumn: int = 0, start: int = 1, rows: int = 20):
        """
        A leaderboard to be returned via discord message

        Arguments:
            columnNames - A list of the names of each column

            data - the raw data of the leaderboard as a list of entries, already sorted by the keyColumn

            keyColumn - the column the table is sorted by, for displaying accurate ranks
        """
        self.data = []
        rowLength = len(columnNames)

        startIndex = start-1
        endIndex = min(startIndex + rows, len(data))
        
        lastRowValue = -1
        rowPlace = 0
        internalRowPlace = 0
        for row in data:
            internalRowPlace += 1
            if len(row) != rowLength:
                raise ValueError("Number of data columns doesn't match the number of column names!")
            
            if row[keyColumn] != lastRowValue:
                rowPlace = internalRowPlace

            self.data.append([str(rowPlace),] + row)
            lastRowValue = row[keyColumn]

        if not endIndex:
            endIndex = len(self.data)

        self.data = self.data[startIndex:endIndex]
            

        self.data = [["#",]+columnNames]+self.data

            
    def getDiscordFormattedMessage(self) -> str:
        """
        Generates the code block leaderboard string, which looks good in discord. Doesn't include a header.

        Returns:
            The code block containing the leaderboard (starting with backticks, ending with backticks)
        """
        for row in self.data:
            color = ""
            match row[0]:
                case "1":
                    color = "\u001b[1;33m"
                case "2":
                    color = "\u001b[1;34m"
                case "3":
                    color = "\u001b[1;32m"

            returnColor = "\u001b[0m"
            row[0] = color+str(row[0])+returnColor

        output = "```ansi\n"+UI.neatTables.generateTable(self.data, 3)+"```"
        return output

        


            


        