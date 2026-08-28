def generateSheet(headers: list[str], columns: list[list]):
    # This is fucking brainrot and spaghetti and bad and to myself in the future: you are a bad person and don't deserve love (until you fix this)
    columnFirstElementSizes = [0 for column in columns]
    columnSecondElementSizes = [0 for column in columns]
    columnThirdElementSizes = [0 for column in columns]
    columnSingleElementSizes = [0 for column in columns]
    subColumnPadding = 2
    for i in range(len(columns)):
        firstElementSize = 0
        secondElementSize = 0
        singleElementSize = 0

        for columnRow in columns[i]:
            if len(columnRow) == 1:  # Single element columns (the maps)
                if len(columnRow[0]) > singleElementSize:
                    singleElementSize = len(columnRow[0])

            elif len(columnRow) == 2:  # Dual element rows (the PBs)
                if len(columnRow[0]) + subColumnPadding > firstElementSize:
                    firstElementSize = len(columnRow[0]) + subColumnPadding

                if len(columnRow[1]) > secondElementSize:
                    secondElementSize = len(columnRow[1])

            elif len(columnRow) == 3:  # Triple element rows
                if len(columnRow[0]) + subColumnPadding > firstElementSize:
                    firstElementSize = len(columnRow[0]) + subColumnPadding

                if len(columnRow[1]) + subColumnPadding > secondElementSize:
                    secondElementSize = len(columnRow[1]) + subColumnPadding

                if len(columnRow[2]) > columnThirdElementSizes[i]:
                    columnThirdElementSizes[i] = len(columnRow[2])

            else:  # Anything more is unsupported
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
                    width = max(
                        columnSingleElementSizes[index],
                        columnFirstElementSizes[index]
                        + columnSecondElementSizes[index]
                        + columnThirdElementSizes[index],
                    )
                    fullRow.append("─" * width)
                else:
                    fullRow.append(row[0])
            elif len(row) == 2:
                fullRow.append(row[0] + " " * (columnFirstElementSizes[index] - len(row[0])) + row[1])
            elif len(row) == 3:
                fullRow.append(
                    row[0]
                    + " " * (columnFirstElementSizes[index] - len(row[0]))
                    + row[1]
                    + " " * (columnSecondElementSizes[index] - len(row[1]))
                    + row[2]
                )
        rows.append(fullRow)

    columnWidths = []
    for index, column in enumerate(columns):
        width = len(headers[index])
        for row in column:
            if len(row) == 1:
                value = row[0]
                if value == "-":
                    value = "─" * max(
                        columnSingleElementSizes[index],
                        columnFirstElementSizes[index]
                        + columnSecondElementSizes[index]
                        + columnThirdElementSizes[index],
                    )
            elif len(row) == 2:
                value = row[0] + " " * (columnFirstElementSizes[index] - len(row[0])) + row[1]
            else:
                value = (
                    row[0]
                    + " " * (columnFirstElementSizes[index] - len(row[0]))
                    + row[1]
                    + " " * (columnSecondElementSizes[index] - len(row[1]))
                    + row[2]
                )
            width = max(width, len(value))
        columnWidths.append(width)

    def formatRow(values: list[str]) -> str:
        formatted = [str(value).ljust(columnWidths[i]) for i, value in enumerate(values)]
        return "│ " + " │ ".join(formatted) + " │"

    border = "╭" + "┬".join("─" * (width + 2) for width in columnWidths) + "╮"
    separator = "├" + "┼".join("─" * (width + 2) for width in columnWidths) + "┤"
    bottom = "╰" + "┴".join("─" * (width + 2) for width in columnWidths) + "╯"

    table_lines = [border]
    table_lines.append(formatRow(headers))
    table_lines.append(separator)
    for row in rows:
        table_lines.append(formatRow(row))
    table_lines.append(bottom)
    return "\n".join(table_lines)


if __name__ == "__main__":
    headers = ["Map", "Record"]
    columns = [[['00/01'], ['02/03'], ['04/05'], ['-'], ['Total']],
               [['2:02.940', 'alatreph', '1'], ['1:07.245', 'nick', '2'], ['59.910', 'sidious', '3'], ['-'], ['69:42.000']],
               ]
    print(generateSheet(headers, columns))
