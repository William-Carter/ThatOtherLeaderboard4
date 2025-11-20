from database.sprmFuncs.pchip import pchip2

xValues = [
    840, 
    870, 
    885, 
    920, 
    970, 
    1080, 
    1440, 
    1920
]

yValues = [
    1190,
    990,
    890,
    690,
    490,
    240,
    90,
    0
]

def func(newValue):
    return pchip2(xValues, yValues, newValue)

def inv(newValue):
    return pchip2(list(reversed(xValues), list(reversed(yValues), newValue)))



