from database.sprmFuncs.pchip import pchip3
from scipy.interpolate import PchipInterpolator
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

ixValues = list(reversed(xValues))
iyValues = list(reversed(yValues))


interpolator = PchipInterpolator(xValues, yValues)
invInterpolator = PchipInterpolator(iyValues, ixValues)


def func(newValue):
    return pchip3(xValues, yValues, interpolator, newValue)

def inv(newValue):
    return pchip3(iyValues, ixValues, invInterpolator, newValue)


