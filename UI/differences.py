import UI.durations
def colourDifference(diff: float, reverse=False) -> str:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    white = "\u001b[0m"

    diff = round(diff, 3)

    formatted = UI.durations.formatted(abs(diff))
    if reverse:
        diff *= -1

    if diff == 0:
        return "+"+formatted
    
    if diff < 0:
        return red+"+"+formatted+white
    
    else:
        return green+"-"+formatted+white


def bold(text: str) -> str:
    """
    Wrap a string in the ANSI formatting code for bold text
    """
    bold = "\u001b[1;37m"
    white = "\u001b[0m"
    return bold + text + white

def underline(text: str) -> str:
    """
    Wrap a string in the ANSI formatting code for underline text
    """
    underline = "\u001b[2;37m"
    white = "\u001b[0m"
    return underline + text + white