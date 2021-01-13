import fetch
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime as dt
from datetime import timedelta 
import numpy as np


(bill, interval) = fetch.dataframe_from_xml()

lastBillReading = bill.iat[bill.shape[0] - 1,0]+bill.iat[bill.shape[0] - 1,1]
currUsage = interval[interval['Start Time'] + interval['Duration'] > lastBillReading]
x = bill["Wh"].to_numpy().reshape((-1, 1))
y = bill["Cost"]

cost = LinearRegression().fit(x,y)
projections = []
i = 0
while (i < currUsage.shape[0] - 1):

    lastSeven = interval[interval['Start Time'] + np.timedelta64(7,'D') >= currUsage.iat[i,0]]
    
    usage= currUsage[:i+1]
    usage = usage["Wh"].sum()
    averageWh = lastSeven.mean()
    

   
    currInterval = currUsage.iat[i,0] - lastBillReading

    period = 30

    percentageOfCycle = currInterval.total_seconds()/(period*24*3600)

    cycleRemaining = 30*(1-percentageOfCycle)

    cycleRemaining *= 48


    estimatedTotalUsage = usage + cycleRemaining * averageWh
    projections.append(cost.predict(estimatedTotalUsage.to_numpy().reshape(-1,1))/100000)
    i += 2
    


plt.plot(projections)

plt.show()


