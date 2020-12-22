#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 13:56:55 2020

@author: ikaheia1
"""
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def __Plot_summary(series):
    desc = series.describe().round().to_frame()
    
    
    fig,ax = plt.subplots(3,2,figsize=(8,8))
    fig.suptitle('Time series summary',fontsize=20,y=1.05)
    
    ax[0,0].plot(series)
    ax[0,0].set_title('Original timeseries')
    ax[0,0].set_xticklabels(ax[0,0].get_xticks(),Rotation= 45) 
    
    ax[0,1].hist(series,20)
    ax[0,1].set_title("Battery level histogram")

    '''
    fig = plt.figure()
    series.plot.box(grid=True,title="Battery level bar plot")
    

    the_table = plt.table(cellText=desc.values,colWidths = [0.25]*len(desc.columns),
          rowLabels=desc.index,
          colLabels=desc.columns,
          cellLoc = 'center', rowLoc = 'center',
          loc='center')

    plt.title("Time series summary")
    the_table.scale(2, 2)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)# Hide axes border
    plt.box(on=None)
    plt.draw()
    plt.show()
    '''
    
    pd.plotting.lag_plot(series,lag=1,ax=ax[1,0])
    ax[1,0].set_title('Lag plot')
    
    
    pd.plotting.autocorrelation_plot(series,ax=ax[1,1])
    ax[1,1].set_xlim([0,240])
    ax[1,1].set_title('Autocorrelation')
    
    sm.graphics.tsa.plot_pacf(series,lags=48,ax=ax[2,0])
    
    sm.graphics.tsa.plot_acf(series,lags=24,ax=ax[2,1])
    
    fig.tight_layout(pad=1.0)
    plt.show()
    
    return None


def Summary_statistics(series):
    
    __Plot_summary(series)
    
    return None