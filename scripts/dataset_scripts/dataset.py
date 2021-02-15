import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import h5py  
from astropy.time import Time
import sys  

sys.path.insert(0, '/home/jovyan/leading_to_phytoplankton/scripts')
import reader as rd

class DataSet:
    
    '''
    Parent Class for all supported datasets (i.e. ATL03, ATL07, MODIS, etc.)
    all sub classes must support the following methods for use in 
    colocated data class
    '''
    
    def __init__(self, boundingbox, timeframe):
        '''
        :param timeframe: datetime
        '''
        self.bounding_box = boundingbox
        self.time_frame = timeframe
        
    def _fmt_coordinates(self):
        # use icepyx geospatial module (icepyx core)
        raise NotImplementedError

    def _fmt_timerange(self):
        '''
        will return list of datetime objects [start_time, end_time]
        '''
        raise NotImplementedError

    def _validate_input(self):
        raise NotImplementedError

    def search_data(self, delta_t):
        raise NotImplementedError

    def visualize(self):
        raise NotImplementedError
    
    def download(self, out_path):
        raise NotImplementedError
    
    def get_meltpond_fraction(self):
        raise NotImplementedError
    
    def get_sea_ice_fraction(self):
        raise NotImplementedError
    
    def get_roughness(self):
        raise NotImplementedError
    
    def _add2colocated_plot(self):
        raise NotImplementedError
