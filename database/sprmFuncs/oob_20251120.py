from database.sprmFuncs.pchip import pchip2

xValues = [
    300,
    320,
    330,
    360,
    415,
    510,
    780,
    1200
]

yValues = [
    1200,
    1000,
    900,
    700,
    450,
    250,
    100,
    0
]

def func(newValue):
    return pchip2(xValues, yValues, newValue)

def inv(newValue):
    return pchip2(list(reversed(xValues), list(reversed(yValues), newValue)))



