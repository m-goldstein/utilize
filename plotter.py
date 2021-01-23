import usageToolbox
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()



def genPlot(timeScale= 'D', history = 0, averageLength = 7 ,dataFrame = usageToolbox.interval):
    #plots the usage  for every unit time scale, going history units past the current reading(use 0 to show current bill period), 
    #with a line showing average usage for the past averageLength timeScale units

    if history == 0:
        df = usageToolbox.crunchDataFrame(timeScale, dataFrame)
        average = usageToolbox.averageUsage(averageLength, timeScale)
        df = df.truncate(before = (usageToolbox.lastBillReading))
    else:
        df = usageToolbox.crunchDataFrame(timeScale, dataFrame)
        average = usageToolbox.averageUsage(averageLength, timeScale)
        df = df.truncate(before = (usageToolbox.recentReading - np.timedelta64(history,timeScale)))
    
    plt.plot(df)
    plt.axhline(y=average, color='r', linestyle='-')

    plt.show()

#def projectionHistory():
    


genPlot('D', 365,5)