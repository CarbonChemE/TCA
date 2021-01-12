#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:50:32 2020

@author:CarbonChemE
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os

import capData
import GitUp


options = Options()
options.headless = True
DRIVER_PATH = '/usr/local/bin/geckodriver'
driver = webdriver.Firefox(options=options,executable_path=DRIVER_PATH)

savename= str(pd.datetime.now().date())
savefolder='./TCAdata'


def getInfo():
    
    driver.get('https://www.theclimbingacademy.com/tca-life/capacity-tracker')
    
    time.sleep(20)

    driver.switch_to.frame("occupancyCounter")

    select = Select(driver.find_element_by_id('gym-switcher'))
    
    capacityStats = {'DateTime':[pd.datetime.now()]}
    
    centers = ['GLA','PST'] 
    
    for center in centers:
        
        select.select_by_value(center)
        
        time.sleep(20)
        
        capacityStats[center+' Count'] = [int(driver.find_element_by_id('count').text)]
        
        capacityStats[center+' Cap'] = [int(driver.find_element_by_id('capacity').text[3:])]
        
    return pd.DataFrame(capacityStats,index=capacityStats['DateTime'])


if savename+'cap.csv' in os.listdir(savefolder):
    
    capacityData = pd.read_csv(savefolder+'/'+savename+'cap.csv',parse_dates=True,index_col=0)
    
else:
    
    capacityData = getInfo()

while True:
    
    try:
        
        time.sleep(840)
    
        #print(str(pd.datetime.now())[:22])
        
        datecheck = str(pd.datetime.now().date())
        
        if datecheck != savename:
            
            newGraphs = capData.getGraphs(savefolder)
            GitUp.updateGraphs(newGraphs)
            
            savename = datecheck # need to save the df and reset it or it will get bigger and bigger and also make the files full of dupication
            capacityData = getInfo()
            
        else:
            capacityData = pd.concat([capacityData,getInfo()])

        capacityData.to_csv(savefolder+'/'+savename+'cap.csv')
        
        
    except:
        #could do with logging errors or printing them
        continue
    

    
    
    
    
    
    
   
    
    
    
    
    