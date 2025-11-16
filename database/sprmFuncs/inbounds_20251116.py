from database.sprmFuncs.pchip import pchip
values = [
        (440, 1200),
        (460, 1000),
        (480, 870),
        (510, 700),
        (570, 500),
        (690, 270),
        (1200, 100),
        (1800, 0)
    ]

def func(newValue):
    return pchip(values, newValue)

def inv(newValue):
    invertedValues = list(reversed([(x[1], x[0]) for x in values]))
    return pchip(invertedValues, newValue)