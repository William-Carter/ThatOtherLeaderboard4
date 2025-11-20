from database.sprmFuncs.pchip import pchip2

xValues = [
    635,
    660,
    680,
    720,
    750,
    870,
    1440,
    1800
]

yValues = [
    1200,
    950,
    800,
    590,
    470,
    200,
    50,
    0
]

def func(newValue):
    return pchip2(xValues, yValues, newValue)

def inv(newValue):
    return pchip2(list(reversed(xValues), list(reversed(yValues), newValue)))



