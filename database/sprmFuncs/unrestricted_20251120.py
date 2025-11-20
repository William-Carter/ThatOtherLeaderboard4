from database.sprmFuncs.pchip import pchip2

xValues = [
    530,
    545,
    570,
    600,
    660,
    780,
    900,
    1440,
    1750
]

yValues = [
    1200,
    1000,
    840,
    700,
    500,
    250,
    150,
    45,
    0
]

def func(newValue):
    return pchip2(xValues, yValues, newValue)

def inv(newValue):
    return pchip2(list(reversed(xValues), list(reversed(yValues), newValue)))



