from database.sprmFuncs.pchip import pchip
values = [
        (530, 1200),
        (545, 1000),
        (570, 840),
        (600, 700),
        (660, 500),
        (780, 250),
        (900, 150),
        (1440, 45),
        (1750, 0)
    ]

def func(newValue):
    return pchip(values, newValue)

def inv(newValue):
    invertedValues = list(reversed([(x[1], x[0]) for x in values]))
    return pchip(invertedValues, newValue)