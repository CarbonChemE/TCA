#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:40:58 2020

@author:CarbonChemE
"""

import pandas as pd

import os

import plotly.express as px

dateValue = {'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5,'Saturday':6,'Sunday':7}


hours = {'GLA':{'Weekday':[7,22],'Weekend':[8,20]},
                'PST':{'Weekday':[10,22],'Weekend':[9,20]}}

## seem to have data on weekends after the normal closing hours

# can i add deviation as error bars?


def grabFiles(filepath='./TCA data'):
      
    
    files=os.listdir(filepath)
    
    dfs = [pd.read_csv(filepath+'/'+file,index_col=0,parse_dates=[0,1]) for file in files]
    
    return pd.concat(dfs)



# stopgap to just pull one file

#just to test on one file#oneFile = pd.read_csv('/home/peter/Desktop/2020-10-10cap.csv',index_col=0,parse_dates=[0,1])


def processDf(df):
    
    
    df = df.copy()
    
    #need to cut out empty data i.e non open hours
    #not sure i need to resample and then group by hour later prob should drop a set oof operations
    df=df.resample('30T').mean().round().copy()
    
    df['DateTime'] = df.index
    
    df['Day'] = df['DateTime'].dt.day_name()
    
    df= df[df['DateTime'].dt.hour.between(7,22)]
    
    return df
    

def groupsMean(df):
    
    ##reallyy need to group by day and time but not date
    
    df = df.copy()
    
    df = df.groupby(['Day',df.index.hour]).mean().dropna()
    
    df = df.reset_index()
    
    df = df.rename(columns={'level_1':'Hour'})
    
    return df
    
   
def sortByDay(df):
    
    df=df.copy()
    
    df['Sort']=df.Day.apply(lambda x:dateValue[x])
    
    df = df.sort_values(['Sort','Hour'])
    
    df.reset_index(inplace=True)
    
    return df.drop('index',axis=1) 
    

    #was dropping the sort col but it is useful to have
    #df = df.drop('Sort',axis=1).reset_index()  
    
    #return df.drop('index',axis=1)   

def outOfHours(df):
        
        cols=list(df.columns)
    
        gyms={'GLA':2,'PST':4}
        
        df=df.copy()
        
        df['Weekday']='Weekday'
        
        df.loc[df['Sort']>5,'Weekday']='Weekend'
        
        for gym in gyms:
        
            for partofweek in hours[gym]:
                
                df.loc[df['Hour']<hours[gym][partofweek][0],cols[gyms[gym]]] = 0
    
                df.loc[df['Hour']>hours[gym][partofweek][1],cols[gyms[gym]]] = 0
                
        return df

def fractionalCap(df):
    df = df.copy()
    
    df['GLA %'] = 100*(df['GLA Count']/df['GLA Cap'])
    
    df['PST %'] = 100*(df['PST Count']/df['PST Cap'])
    
    return df



def avsByDay(filepath):
    
    #need to get rid of the out of hours data
    
    df = grabFiles(filepath)
    
    dftidy= processDf(df)
    
    dftidy= groupsMean(dftidy)
    
    dftidy = sortByDay(dftidy) 
    
    dftidy = outOfHours(dftidy)
    
    return fractionalCap(dftidy)
    
    


 # need to sort the days so that it goes monday tuesday etc or get a day slicer   
def getGraphs(filepath):
    

    data = avsByDay()
    
    graphN = px.line(data,x='Hour',
                     y='GLA %',color='Day',
                     facet_col='Day',title='NRoom',
                     labels={'GLA %':'Mean Occupancy %','Hour':'Time'})
    
    graphP = px.line(data,x='Hour',
                     y='PST %',color='Day',
                     facet_col='Day',title='PStore',
                     labels={'PST %':'Mean Occupancy %','Hour':'Time'})
    
    
    #graphN.write_html('/home/peter/Desktop/PyProject/NRoom.html')
    #graphP.write_html('/home/peter/Desktop/PyProject/PStore.html')
    
    return {'PStore.html':graphP.to_html(),'NRoom.html':graphN.to_html()}

#cols= list(df.columns)

    


#oneFile.plot(y=cols[1:5])


