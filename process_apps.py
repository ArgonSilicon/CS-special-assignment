#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:08:26 2020

@author: arsi
"""

# standard library imports
import os
from pathlib import Path
import json

# change correct working directory
WORK_DIR = Path(r'/home/arsi/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

# third party imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Local application import


from vector_encoding import ordinal_encoding, one_hot_encoding, decode_string, decode_string_3, custom_resampler, normalize_values
from calculate_RQA import Calculate_RQA
from plot_recurrence import Show_recurrence_plot
from save_results import dump_to_json
from plot_timeseries import show_timeseries_scatter, show_features
from save2mat import save2mat
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from json_load import load_one_subject
from Plot_similarity import Plot_similarity
from interpolate_missing import interpolate_missing

def process_apps(df):
    
    # parameters
    ED = 4 # embedding dimensions
    TD = 1 # time delay
    RA = 0.05 # neigborhood radius
       
    # Load dictionary for app labels
    DICT_PATH = Path(r'/home/arsi/Documents/SpecialAssignment/CS-special-assignment/')
    DICT_NAME = 'labels_dict.json'
    loadname = DICT_PATH / DICT_NAME
    _,labels = load_one_subject(loadname)
    
    #%%
    df['Encoded'] = ordinal_encoding(df['application_name'].values.reshape(-1,1))
    df['group'] = [labels[value] for value in df['application_name'].values]
    df['Encoded_group'] = ordinal_encoding(df['group'].values.reshape(-1,1))
    
    #enc_df = pd.DataFrame(one_hot_encoding(df0['Encoded_group'].values.reshape(-1,4)))
    Colnames = ['Communication','Entertainment','Other','Sports','Work/Study']
    enc_df = pd.DataFrame(one_hot_encoding(df['Encoded_group'].values.reshape(-1,1)),columns=Colnames,index=df.index)
    df = pd.concat([df,enc_df], axis=1, join='outer') 
    df_filt = df.filter(["time",*Colnames])
    resampled = df_filt.resample("H").sum()
    #resampled = resampled.drop(columns='Other')
    
    timeseries = resampled.to_numpy()
    #%%
    res, mat = Calculate_RQA(timeseries,ED,TD,RA)
    sim = calculate_similarity(timeseries,'euclidean')
    nov = compute_novelty_SSM(sim)
    Plot_similarity(sim,nov)

    #%% show recursion plot and save figure
    # set correct names and plot title
    FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "recplot_0"
    TITLE = "AppNotifications Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
    Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)
    
    # set correct names and save metrics as json 
    RESPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Metrics/')
    RESNAME = "metrics_0.json"
    dump_to_json(res,RESPATH,RESNAME)  
    
    # save the timeseries
    TSPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Timeseries/')
    TSNAME = "timeseries_0.mat"
    save2mat(df['Encoded'].values,TSPATH,TSNAME)        
    
    #% Plot timeseries and save figureShow_recurrence_plot(sim2)
    FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
    FIGNAME = "timeseries_0_scatter"
    show_timeseries_scatter(df.index,df.Encoded_group,"Application usage","time","Applications",FIGPATH,FIGNAME)
    
    #%% Extract features from timeseries, plot, and save
    
    #FIGNAME = "features_0"
    show_features(resampled['Communication'],"Comm","xlab","ylab")
    show_features(resampled['Entertainment'],"Entertainment","xlab","ylab")
    show_features(resampled['Other'],"Other","xlab","ylab")
    show_features(resampled['Sports'],"Sports","xlab","ylab")
    show_features(resampled['Work/Study'],"Work/Study","xlab","ylab")
    
    return df
if __name__ == "__main__":
    pass