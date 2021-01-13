"""Parse GreenButton XML (within zipfile)"""

import datetime
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 
import pdb


package_directory = os.path.dirname(os.path.abspath(__file__))
XMLFILE = os.path.join(package_directory, 'interval.xml')
BILLFILE = os.path.join(package_directory, 'billing.xml')


ns = {'default': 'http://www.w3.org/2005/Atom',
    'reading': 'http://naesb.org/espi'}


    
def usage_point():
    tree = ET.parse(XMLFILE)
    root = tree.getroot()
    
    return root.findall('default:entry/default:content/reading:UsagePoint',ns)
    
def start_date_from_interval_block(interval_block_node):
    """ Return start date as DATETIME from interval block xml node """
    start_date_node = interval_block_node.find('reading:interval/reading:start',ns)
    return datetime.datetime.utcfromtimestamp(int(start_date_node.text))
    
def end_date_from_interval_block(interval_block_node):
    """ Return end date as DATETIME from interval block xml node """
    start_date = start_date_from_interval_block(interval_block_node)
    duration_text = interval_block_node.find('reading:interval/reading:duration',ns).text
    duration = datetime.timedelta(seconds=duration_text)
    return start_date + duration
    
def get_interval_blocks(root):
    """ Return list of interval blocks """
    return root.findall('default:entry/default:content/reading:IntervalBlock',ns)
     
def get_interval_readings(interval_block):
    """ Return list of interval readings """
    return interval_block.findall('reading:IntervalReading',ns)

def parse_reading(interval_reading_node, bill = True):
    ##cost = int(interval_reading_node.find('reading:cost',ns).text)
    if bill:
        start = datetime.datetime.utcfromtimestamp(int(interval_reading_node.find('reading:timePeriod/reading:start',ns).text))
        duration = datetime.timedelta(seconds = int(interval_reading_node.find('reading:timePeriod/reading:duration',ns).text))
        value = int(interval_reading_node.find('reading:value',ns).text)
        cost = int(interval_reading_node.find('reading:cost',ns).text)
    
        return (start, duration, value,cost)
    else:
        start = datetime.datetime.utcfromtimestamp(int(interval_reading_node.find('reading:timePeriod/reading:start',ns).text))
        duration = datetime.timedelta(seconds = int(interval_reading_node.find('reading:timePeriod/reading:duration',ns).text))
        value = int(interval_reading_node.find('reading:value',ns).text)
        return (start, duration, value)
    
    
def dataframe_from_xml():
   
    tree = ET.parse(XMLFILE)
    root = tree.getroot()

    interval_blocks = get_interval_blocks(root)

    intReadings = []

    for interval_block in interval_blocks:
        for interval_reading in get_interval_readings(interval_block):
            intReadings.append(parse_reading(interval_reading,False))
    

    tree = ET.parse(BILLFILE)
    root = tree.getroot()

    interval_blocks = get_interval_blocks(root)

    billReadings = []

    for interval_block in interval_blocks:
        for interval_reading in get_interval_readings(interval_block):
            billReadings.append(parse_reading(interval_reading))
 
    return (pd.DataFrame(billReadings,columns=['Start Time','Duration','Wh','Cost']),pd.DataFrame(intReadings,columns=['Start Time','Duration','Wh']))
    



