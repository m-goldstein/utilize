import usageToolbox
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()



def genPlot(timeScale= 'D', history = 0, averageLength = 7 ,dataFrame = usageToolbox.interval):
    #plots the usage  for every unit time scale, going history units past the current billing interval, 
    #with a line showing average usage for the past averageLength timeScale units

    df = usageToolbox.crunchDataFrame(timeScale, dataFrame)
    average = usageToolbox.averageUsage(averageLength, timeScale)

    df = df.truncate(before = (usageToolbox.lastBillReading - np.timedelta64(history,timeScale)))
    predictNow()
    
    plt.plot(df)
    plt.axhline(y=average, color='r', linestyle='-')

    plt.show()

def predictNow():
    #predict the usage for the last incomplete datapoint
    return None

print(usageToolbox.projectUsage())
genPlot('M',12,12)