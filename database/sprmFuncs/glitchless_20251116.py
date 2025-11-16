from database.sprmFuncs.pchip import pchip
values = [
        (840, 1190),
        (870, 990),
        (885, 890),
        (920, 690),
        (970, 490),
        (1080, 240),
        (1440, 90),
        (1920, 0)
        ]

def func(newValue):
    return pchip(values, newValue)

def inv(newValue):
    invertedValues = list(reversed([(x[1], x[0]) for x in values]))
    return pchip(invertedValues, newValue)