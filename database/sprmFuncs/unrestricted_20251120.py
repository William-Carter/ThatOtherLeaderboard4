from database.sprmFuncs.pchip import pchip3
from scipy.interpolate import PchipInterpolator
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

ixValues = list(reversed(xValues))
iyValues = list(reversed(yValues))


interpolator = PchipInterpolator(xValues, yValues)
invInterpolator = PchipInterpolator(iyValues, ixValues)


def func(newValue):
    return pchip3(xValues, yValues, interpolator, newValue)

def inv(newValue):
    return pchip3(iyValues, ixValues, invInterpolator, newValue)


