import fetch
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime as dt
from datetime import timedelta 
import numpy as np

period = 30
readingsPerHour = 2

(bill, interval) = fetch.dataframe_from_xml()

lastBillReading = bill.iat[bill.shape[0] - 1,0]+bill.iat[bill.shape[0] - 1,1]
currUsage = interval[interval['Start Time'] + interval['Duration'] > lastBillReading]

x = bill["Wh"].to_numpy().reshape((-1, 1))
y = bill["Cost"]
cost = LinearRegression().fit(x,y)

    
def projectUsage():
    
    usage = currUsage.sum()
    averageWh = averageUsage(7,'D')
   
    currInterval = currUsage.iat[currUsage.shape[0]-1,0] - currUsage.iat[0,0] 
    percentageOfCycle = currInterval.total_seconds()/(period*24*3600)
    cycleRemaining = period*(1-percentageOfCycle)
   
    return (estimateCost(usage + cycleRemaining * averageWh))
    

def estimateCost(amountUsed):
    return cost.predict(amountUsed.to_numpy().reshape(-1,1))/100000

def crunchDataFrame(timescale,df):
    df.set_index(df['Start Time'],inplace = True)
    return df['Wh'].resample(timescale).sum()


def averageUsage(units, timeScale):
    #Crunch the dataframe so we can drop the last incomplete average reading
    lastReading = currUsage.iat[currUsage.shape[0] -1, 0]
    df = crunchDataFrame(timeScale, interval)
    df.drop(df.tail(1).index,inplace=True)
   
   
    return (df.truncate(before = (lastReading - np.timedelta64(units,timeScale))).mean())
    


