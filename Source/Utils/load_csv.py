#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:06:32 2020

@author: arsii

Load all .csv files in a given folder. The files are loaded as pandas 
dataframes which are stored in a ictionary. All the subfolders in the given 
folder are ignored. If there is file of a type other than csv in the folder, 
an exception is raised.

"""

import pandas as pd
from os import listdir
from os.path import isfile, join, exists

def _convert_to_datetime(date, units = 'ms'):
    """
    Convert a given pandas series from unix time to datetime.

    Parameters
    ----------
    date : pandas series
        Dataframe column containing the time
    units : str (default = 'ms')
        Time unit conversion type
    
    Returns
    -------
    conv_date : pandas series
        Datetime converted pandas series
    
    """
    assert isinstance(date,pd.core.series.Series), "Timeseries should be Pandas series type."
    assert isinstance(units,str), "Unit type should be str, not {}".format(type(units))
    
    conv_date = pd.to_datetime(date,unit = units)
    return conv_date

def _convert_time(df, colname = None, conv_type = 's'):
    """ 
    Convert dataframe time to pandas datetime object and set the corrensponding column as a dataframe index.

    Parameters
    ----------
    df : pandas dataframe
        pandas dataframe 
    colname : str, optional
        Name of the column to be converted. The default is None.

    Returns
    -------
    df : pandas dataframe
        pandas datafrane with converted column

    """
    if colname == None:
        names = [('time','s'),('day','D'),('timestamp','s')]
        for name in names:
            if name[0] in df.columns:
                try: 
                    df[name[0]] = _convert_to_datetime(df[name[0]],name[1])
                except:
                    print('Cannot convert column named: \"{}\" to datetime.'.format(name[0]))
                df = df.set_index(name[0])
                
    else:
        try:
            
            df[colname] = _convert_to_datetime(df[colname],conv_type)
            df = df.set_index(colname)
        except:
                print('Cannot convert column named: \"{}\" to datetime.'.format(name[0]))
    return df

    
def load_one_subject(open_name):
    """
    Load an arbitrary .csv file and return it as a pandas dataframe.

    Parameters
    ----------
    openname : Path -object
        path to the .csv file

    Returns
    -------
    file_name : str
        Name of the given file without suffix

    df: pandas dataframe
        a pandas dataframe created from the read csv file

    """
    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file)
        df = _convert_time(df)
        file_name = open_name.stem
        return file_name, df
    

def load_all_subjects(foldername):
    """
    Load all .csv files in a given folder, and return a dictionary containing the files.

    Parameters
    ----------
    foldername : Path -object
        path to the folder containing .csv files

    Returns
    -------
    csv_dict : dictionary 
        a dictionary containing readed .csv files, 
        filenames used as dict keys.

    """
    if exists(foldername):
        file_list = [f for f in listdir(foldername) if isfile(join(foldername, f))]
        
    else:
        raise Exception("Requested folder: " + str(foldername) + " does not exist.") 
    
    csv_dict = {}
    
    for filename in file_list:
        open_name = foldername / filename
        assert open_name.suffix == ".csv", "Trying to load incorrect file format."
        file_name, csv_file = load_one_subject(open_name)
        csv_dict[file_name] = csv_file
    
    
    if csv_dict:
        return csv_dict
    else:
        raise Exception("There is no files in the selected folder.")
       
    
if __name__ == "__main__":
    pass
    