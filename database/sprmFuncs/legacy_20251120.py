from database.sprmFuncs.pchip import pchip3
from scipy.interpolate import PchipInterpolator
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

ixValues = list(reversed(xValues))
iyValues = list(reversed(yValues))


interpolator = PchipInterpolator(xValues, yValues)
invInterpolator = PchipInterpolator(iyValues, ixValues)


def func(newValue):
    return pchip3(xValues, yValues, interpolator, newValue)

def inv(newValue):
    return pchip3(iyValues, ixValues, invInterpolator, newValue)


