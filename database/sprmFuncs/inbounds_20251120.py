from database.sprmFuncs.pchip import pchip2

xValues = [
    440,
    460,
    480,
    510,
    570,
    690,
    1200,
    1800
]

yValues = [
    1200,
    1000,
    870,
    700,
    500,
    270,
    100,
    0
]

def func(newValue):
    return pchip2(xValues, yValues, newValue)

def inv(newValue):
    return pchip2(list(reversed(xValues), list(reversed(yValues), newValue)))



