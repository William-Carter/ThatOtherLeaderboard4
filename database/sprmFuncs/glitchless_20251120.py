from database.sprmFuncs.pchip import pchip3
from scipy.interpolate import PchipInterpolator

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

ixValues = list(reversed(xValues))
iyValues = list(reversed(yValues))


interpolator = PchipInterpolator(xValues, yValues)
invInterpolator = PchipInterpolator(iyValues, ixValues)


def func(newValue):
    return pchip3(xValues, yValues, interpolator, newValue)

def inv(newValue):
    return pchip3(iyValues, ixValues, invInterpolator, newValue)



