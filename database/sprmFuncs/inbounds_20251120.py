from database.sprmFuncs.pchip import pchip3
from scipy.interpolate import PchipInterpolator
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

ixValues = list(reversed(xValues))
iyValues = list(reversed(yValues))


interpolator = PchipInterpolator(xValues, yValues)
invInterpolator = PchipInterpolator(iyValues, ixValues)


def func(newValue):
    return pchip3(xValues, yValues, interpolator, newValue)

def inv(newValue):
    return pchip3(iyValues, ixValues, invInterpolator, newValue)


