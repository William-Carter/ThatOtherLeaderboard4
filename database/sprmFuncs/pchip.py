from scipy.interpolate import PchipInterpolator
def pchip(values, newValue):
    maximum = values[-1]
    minimum = values[0]
    if newValue >= maximum[0]:
        return maximum[1]
    
    if newValue <= minimum[0]:
        return minimum[1]

    xValues = [value[0] for value in values]
    yValues = [value[1] for value in values]
    interpolator = PchipInterpolator(xValues, yValues)
    return interpolator(newValue)