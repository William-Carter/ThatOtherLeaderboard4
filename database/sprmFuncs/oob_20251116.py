from database.sprmFuncs.pchip import pchip
values = [
        (300, 1200), 
        (320, 1000),
        (330, 900),
        (360, 700),
        (415, 450),
        (510, 250),
        (780, 100),
        (1200, 0)
        ]
def func(newValue):
    return pchip(values, newValue)

def inv(newValue):
    invertedValues = list(reversed([(x[1], x[0]) for x in values]))
    return pchip(invertedValues, newValue)