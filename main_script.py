# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is main file


"""
import os
from pathlib import Path

WORK_DIR = Path(r'C:/Users/arsii/Documents/Work/Code/')
os.chdir(WORK_DIR)

import numpy as np
from csv_load import load_all_subjects, load_one_subject
from rolling_stats import convert_to_datetime, resample_dataframe
from plot_recurrence import Create_recurrence_plot, Create_cross_recurrence_plot, Show_recurrence_plot, Save_recurrence_plot
from vector_encoding import ordinal_encoding, one_hot_encoding, decode_string, decode_string_3, custom_resampler
from pyunicorn.timeseries import RecurrencePlot, CrossRecurrencePlot

#%%
DATA_FOLDER = Path(r'C:/Users/arsii/Documents/Work/Data/CSV/')
csv = load_all_subjects(DATA_FOLDER)

#%%
dict_keys = list(csv.keys())

'''
Dict keys:
    0 = App notifications 
    1 = Battery level
    2 = ESM
    3 = Location / day
    4 = Screen status
'''
##############################################################################
#%% App notifications
df0 = csv[dict_keys[0]]
# put these on import!!!
df0['time'] = convert_to_datetime(df0['time'],'s')
df0 = df0.set_index("time")
#%% filter
df0_filt = df0.filter(["time","application_name",])
values0 = ordinal_encoding(df0_filt['application_name'].values.reshape(-1,1))

#%%
rp0 = Create_recurrence_plot(values0,0.25)
rm0 = rp0.recurrence_matrix()
Show_recurrence_plot(rm0)

##############################################################################
#%% Battery level
df1 = csv[dict_keys[1]]
# put these on import!!!
df1['time'] = convert_to_datetime(df1['time'],'s')
df1 = df1.set_index("time")
#%% filter
df1_filt = df1.filter(["time","battery_level",])
resampled = df1_filt.resample("H").mean()
values1 = resampled.values
#%%
rp1 = Create_recurrence_plot(values1,0.15)
rm1 = rp1.recurrence_matrix()
Show_recurrence_plot(rm1)

##############################################################################
#%% ESM data
df2 = csv[dict_keys[2]]
# put these on import!!!
df2['time'] = convert_to_datetime(df2['time'],'s')
df2 = df2.set_index("time")
# decode answer values
mask1 = df2["type"] == 1
mask2 = df2["type"] == 2
mask3 = df2["type"] == 3
df2.loc[mask1,"answer"] = df2.loc[mask1,"answer"].map(decode_string)
df2.loc[mask2,"answer"] = df2.loc[mask2,"answer"].map(decode_string)
df2.loc[mask3,"answer"] = df2.loc[mask3,"answer"].map(decode_string_3)

#%%
df2_filt = df2.filter(["time","answer",])
df2_filt = df2_filt["answer"].astype(int)
resampled2 = df2_filt.resample("D").apply(custom_resampler)
#%%
values2 = resampled2.values
values2 = np.stack(values2[:-1])
#%%
rp2 = Create_recurrence_plot(values2,0.15)
rm2 = rp2.recurrence_matrix()
Show_recurrence_plot(rm2)

##############################################################################
#%% Location / day ??
df3 = csv[dict_keys[3]]
# put these on import!!!
df3 = df3.set_index("day")
values3 = df3["totdist"].values
#%%
rp3 = Create_recurrence_plot(values3,0.15)
rm3 = rp3.recurrence_matrix()
Show_recurrence_plot(rm3)


##############################################################################
#%% Screen events
df4 = csv[dict_keys[4]]
# put these on import!!!
df4['time'] = convert_to_datetime(df4['time'],'s')
df4 = df4.set_index("time")
#%% filter
df4_filt = df4.filter(["time","screen_status",])
resampled4 = df4_filt.resample("H").count()
resampled41 = df4_filt.resample("D").mean()
values41 = resampled41.values
values4 = resampled4.values
#%%
rp4 = Create_recurrence_plot(values4,0.15)
rm4 = rp4.recurrence_matrix()
Show_recurrence_plot(rm4)


##############################################################################
#%% Test Cross Recurrence
## Battery level / screen events

crp0 = CrossRecurrencePlot(values1,values4,threshold=0.15)
crp0m = crp0.recurrence_matrix()
Show_recurrence_plot(crp0m)
'''
#%% ESM / screen
 
crp1 = Create_cross_recurrence_plot(values2,values4,0.05)
crp1m = crp1.recurrence_matrix()
Show_recurrence_plot(crp1m)

#%% ESM / screen
 
crp1 = Create_cross_recurrence_plot(values2,values41,1)
crp1m = crp1.recurrence_matrix()
Show_recurrence_plot(crp1m)
'''