#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 22:29:40 2020

@author: nabib
"""

### Import modules
import sys
### Add path to scripts
if '/Users/nabib/Documents/github/leading_to_phytoplankton/scripts/' not in sys.path:
    sys.path.insert(0, '/Users/nabib/Documents/github/leading_to_phytoplankton/scripts/')
    

import numpy as np
from astropy.time import Time
import matplotlib.pyplot as plt
import h5py, pyproj
import reader as rd
import cartopy.crs as ccrs
import rasterio
from rasterio.plot import show
import warnings
warnings.filterwarnings('ignore')

# Libraries for working with argo float data
#import pandas as pd
#import matplotlib as mpl

#%% Define path to sample data
data_loc = "/Users/nabib/projects/leading2phytoplankton/data/"


#%% Load IS2 sample data
f_atl03 = data_loc + "ATL03_20190726213326_04400404_003_01.h5"

f = h5py.File(f_atl03, 'r')
# check to see if it is forward (1)  or backward (0) orientation to know which beam is strong/weak. 
# (2 is transition phase- don't use these data)
print(f['orbit_info/sc_orient'][0])

beam = 'gt2l'
df03_full = rd.getATL03(f,beam)
print(df03_full.head())

print("Number of point measurements:", len(df03_full))

### Downsample ATL03 to speed up
df03 = df03_full[::1000]
print("Number of point measurements:", len(df03))

### Convert GPS time to UTC time
epoch = f['/ancillary_data/atlas_sdp_gps_epoch'][0]
df03['time'] = Time(epoch + df03['dt'],format='gps').utc.datetime

### Calculate along track distance relative to the beginning of the cut segment
df03['AT_dist'] = df03.x - df03.x.values[0]

### Read orbit number
df03['orbit_number'] = [f['/orbit_info/orbit_number'][0]] * len(df03)
df03.head()


#%% Load and plot Argo Float Data
# argo_arc_fn = data_loc+'argo_arc.csv'
# argo_ant_fn = data_loc+'argo_ant.csv'

# Load the csv file with Pandas
# argo_arc_df = pd.read_csv(argo_arc_fn)
# argo_ant_df = pd.read_csv(argo_ant_fn)
# # Add column names defined in the metadata
# argo_arc_df.columns = ['lat', 'lon', 'year', 'month', 'day', 'hour', 
#                    'minute', 'Depth (m)', 'bbp (700 nm)', 'temperature', 
#                    'salinity', 'chlorophyll']
# argo_ant_df.columns = ['lat', 'lon', 'year', 'month', 'day', 'hour', 
#                    'minute', 'Depth (m)', 'bbp (700 nm)', 'temperature', 
#                    'salinity', 'chlorophyll']

# # Create a scatter plot showing data locations
# plt.figure(figsize=(8,8), dpi= 90)
# ax = plt.axes(projection=ccrs.PlateCarree()) # choose polar sterographic for projection
# ax.coastlines(resolution='50m', color='black', linewidth=1)
# plt.scatter(argo_arc_df['lon']s, argo_arc_df['lat'], c= 'r',s=1,transform=ccrs.PlateCarree())
# plt.scatter(argo_ant_df['lon'], argo_ant_df['lat'], c= 'r',s=1,transform=ccrs.PlateCarree())
# ax.set_title('Location of Argo Floats');

#%% Load in an example colocated Sentinel-2 Image and determine the bounding box
s2_fn = data_loc + '20190726_T14XMQ.tif'
s2_img = rasterio.open(s2_fn)
s2_bounds  = s2_img.bounds

# Plot S2 image
show(s2_img.read(), transform=s2_img.transform)
#%% Plot ATL03 data with S2 bounding box on top
from shapely.geometry import box
geom = box(*s2_bounds)
print(geom.wkt)
print(s2_img.crs)

var= 'heights' #choose which variable we want to plot

## Set colorbar parameters based on the chosen variable
vmin=-10
vmax=30
ticks=np.arange(-20,100,5)
proj = pyproj.Proj('+init=' + str(s2_img.crs))

plt.figure(figsize=(8,8), dpi= 600)
ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=0)) # choose polar sterographic for projection
ax.coastlines(resolution='50m', color='black', linewidth=1)
ax.set_extent([-180, 180, 60, 90], ccrs.PlateCarree())
#plt.scatter(argo_arc_df['lon'], argo_arc_df['lat'], c= 'r',s=2,transform=ccrs.PlateCarree())
plt.scatter(df03['lons'], df03['lats'],c=df03[var], cmap='viridis', vmin=vmin,vmax=vmax,transform=ccrs.PlateCarree())
plt.plot(*geom.exterior.xy, color='black', linewidth=1,transform=ccrs.UTM(14))
plt.colorbar(label=var, shrink=0.5, ticks=ticks,extend='both');

#%% Show where ICESat-2 granule crosses the corresponding colocated Sentinel-2 image

# Plot uncropped array
f, ax = plt.subplots(figsize=(8,8), dpi= 600)

show(s2_img.read(), transform=s2_img.transform, ax = ax, adjust = 'linear')

x, y = proj(np.array(df03['lons']), np.array(df03['lats']))
plt.plot(x[-1500:], y[-1500:], '.r')

plt.show()

#%% Show zoomed in on pond
f, ax = plt.subplots(figsize=(8,8), dpi= 600)
show(s2_img.read(), transform=s2_img.transform, ax = ax)
x_zoom, y_zoom = proj(np.array(df03_full['lons'][-1500000:]), np.array(df03_full['lats'][-1500000:]))
plt.plot(x_zoom, y_zoom, '.r')

plt.xlim((425027.75573844597, 427825.9806155204))
plt.ylim((8970799.98349305, 8972896.74600312))

lonmin, latmin = proj(plt.xlim()[0], plt.ylim()[0], inverse=True)
lonmax, latmax = proj(plt.xlim()[1], plt.ylim()[1], inverse=True)
print("lonmin:", lonmin)
print("lonmax:", lonmax)
print("latmin:", latmin)
print("latmax:", latmax)
