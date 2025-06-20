import tabulate

def generateSheet(headers: list[str], columns: list[list]):
    columnFirstElementSizes = [0 for column in columns]
    columnSecondElementSizes = [0 for column in columns]
    columnSingleElementSizes = [0 for column in columns]
    subColumnPadding = 2
    for i in range(len(columns)):
        firstElementSize = 0
        secondElementSize = 0
        singleElementSize = 0

        for columnRow in columns[i]:
            if len(columnRow) == 1: # Single element columns (the maps)
                if len(columnRow[0]) > singleElementSize:
                    singleElementSize = len(columnRow[0])

            elif len(columnRow) == 2: # Dual element rows (the PBs)
                if len(columnRow[0])+subColumnPadding > firstElementSize:
                    firstElementSize = len(columnRow[0])+subColumnPadding

                if len(columnRow[1]) > secondElementSize:
                    secondElementSize = len(columnRow[1])

            else: # Anything more is unsupported
                raise Exception("Too many elements provided in a cell!")

        columnFirstElementSizes[i] = firstElementSize
        columnSecondElementSizes[i] = secondElementSize
        columnSingleElementSizes[i] = singleElementSize

    rows = []
    for i in range(len(columns[0])):
        fullRow = []
        for index, column in enumerate(columns):
            row = column[i]
            if len(row) == 1:
                if row[0] == "-":
                    width = max(columnSingleElementSizes[index], (columnFirstElementSizes[index]+columnSecondElementSizes[index]))
                    fullRow.append("-"*width)
                else:
                    fullRow.append(row[0])
            elif len(row) == 2:
                fullRow.append(row[0] + " "*(columnFirstElementSizes[index]-len(row[0])) + row[1])
        rows.append(fullRow)

    print(rows)

    print(tabulate.tabulate(rows, headers, tablefmt="simple_grid"))



if __name__ == "__main__":
    headers = ["Map", "Glitchless", "Inbounds", "Out of Bounds"]
    columns = [[["00/01"], ["02/03"], ["04/05"], ["-"]], 
               [["2:02.940", "3rd"], ["1:07.245", "2nd"], ["59.910","3rd"], ["-"]],
               [["1:10.890", "4th"], ["56.490", "2nd"], ["58.275", "11th"], ["-"]]
               ]
    generateSheet( headers, columns)

