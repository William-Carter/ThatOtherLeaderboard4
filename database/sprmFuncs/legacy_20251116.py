from database.sprmFuncs.pchip import pchip
values = [
        (635, 1150),
        (660, 950),
        (680, 800),
        (720, 590),
        (750, 470),
        (870, 200),
        (1440, 50),
        (1800, 0)
    ]
def func(newValue):
    return pchip(values, newValue)

def inv(newValue):
    invertedValues = list(reversed([(x[1], x[0]) for x in values]))
    return pchip(invertedValues, newValue)