#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Read and plot EPA and Purple site

"""
__author__ = "Nastaran Moghimi"
__copyright__ = "Copyright 2017, UCAR/NOAA"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "nastarann.moghimi@gmail.com"


import matplotlib.pyplot as plt
import numpy as np
import os,sys
import datetime
import string
import pandas as pd
#import geopandas as gpd
#import fiona

from    collections import defaultdict

#live maps
import folium
#import mplleaflet

#static maps
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import (LONGITUDE_FORMATTER,
                                   LATITUDE_FORMATTER)
import cartopy.feature as cfeature 
from matplotlib.offsetbox import AnchoredText


###functions
def get_ind(lim,lons,lats):
    
    [ind] = np.where((lons > lim['xmin']) & 
                    ( lons < lim['xmax']) & 
                    ( lats > lim['ymin']) & 
                    ( lats < lim['ymax']))
    
    return ind


def make_map(projection=ccrs.PlateCarree()):                                                                                                                                        
                                                                                           
    """                                                                          
    Generate fig and ax using cartopy                                                                    
    input: projection                                                                                    
    output: fig and ax                             
    """                                  
    alpha = 0.5                                        
    subplot_kw = dict(projection=projection)                        
    fig, ax = plt.subplots(figsize=(9, 13),                           
                           subplot_kw=subplot_kw)   
    gl = ax.gridlines(draw_labels=True)                                 
    gl.xlabels_top = gl.ylabels_right = False 
    gl.xformatter = LONGITUDE_FORMATTER                        
    gl.yformatter = LATITUDE_FORMATTER                                
                                    
        # Put a background image on for nice sea rendering.             
    ax.stock_img()                                   
                                                          
    # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
    states_provinces = cfeature.NaturalEarthFeature(                      
        category='cultural',                  
        name='admin_1_states_provinces_lines',
        scale='50m',           
        facecolor='none')        

    SOURCE = 'Natural Earth'
    LICENSE = 'public domain'
                                                                                                                                                                                    
    ax.add_feature(cfeature.LAND,zorder=0,alpha=alpha)          
    ax.add_feature(cfeature.COASTLINE,zorder=1,alpha=alpha)
    ax.add_feature(cfeature.BORDERS,zorder=1,alpha=2*alpha)
                       
    ax.add_feature(states_provinces, edgecolor='gray',zorder=1)
                                                          
    # Add a text annotation for the license information to the
    # the bottom right corner.                                            
    text = AnchoredText(r'$\mathcircled{{c}}$ {}; license: {}'
                        ''.format(SOURCE, LICENSE),
                        loc=4, prop={'size': 9}, frameon=True)                                    
    ax.add_artist(text)                                                                           
                                         
    ax.set_xlim(-132,-65)  #lon limits           
    ax.set_ylim( 20 , 55)  #lat limits   
    return fig, ax



#### MAIN
region = defaultdict(dict)
#####
name = 'US'
region[name]['xmin']  = -125.0
region[name]['xmax']  = -55.
region[name]['ymin']  =  20.0
region[name]['ymax']  =  52.0

name = 'Texas'
region[name]['xmin']  = -107.0
region[name]['xmax']  = -92.9
region[name]['ymin']  =  24.0
region[name]['ymax']  =  38.1


name = 'Arizona'
region[name]['xmin']  = -114.85
region[name]['xmax']  = -108.9
region[name]['ymin']  =  31.1
region[name]['ymax']  =  37.1


name = 'California'
region[name]['xmin']  = -125.1
region[name]['xmax']  = -113.8
region[name]['ymin']  =  31.0
region[name]['ymax']  =  42.55


#####################################################

names = ['US', 'Arizona', 'California', 'Texas']
#names = ['US']



inp_dir = 'inp/'

print ('Read ...')
purple_stations_info_file = inp_dir + 'PurpleAir_EPA_list.csv'
purp_infos = pd.read_csv(purple_stations_info_file)


grp = purp_infos.groupby(purp_infos.epa_indx)


for name in names:
    #get lim
    lim = region[name]

    #plot stations
    print ('Static Cartopy map ...')
    for group in ['PM2.5', 'PM10' ]:
        
        print (name , group) 
        df = grp.get_group(group)
        fig,ax = make_map()                                             
        ax.set_title('Location of ' + group + ' for EPA and Purple stations in '+ name +'(#'+str(len(df.epa_lat))+')')
        ax.scatter(x = df.epa_lon , y = df.epa_lat ,s=40,lw=0, c= 'red' , label = 'EPA'    ,alpha=0.85)
        ax.scatter(x = df.p_lon   , y = df.p_lat   ,s=10,lw=0, c= 'blue', label = 'Purple' ,alpha=0.85)
        ax.legend(ncol=4)
        ax.legend()  
        ax.set_xlim(lim['xmin'],lim['xmax'])
        ax.set_ylim(lim['ymin'],lim['ymax'])
        plt.savefig(name+'_'+group + '_stations.png',dpi=600)
        plt.close('all')




#All in the same map

for name in names:
    #get lim
    lim = region[name]

    #plot stations
    print ('Static Cartopy map ...')
    fig,ax = make_map()                                             
    for group in ['PM2.5', 'PM10' ]:
        print (name , group) 
        df = grp.get_group(group)
        
        if   group == 'PM2.5':
            epa_lab = 'EPA PM2.5'    + ' (#'+str(len(df.epa_lat))+')'
            epa_col = 'r'
            epa_mar = 's'
            
            pur_lab = 'Purple PM2.5' +' (#'+str(len(df.epa_lat))+')'
            pur_col = 'k'
            pur_mar = '+'
            
        elif group == 'PM10':
            epa_lab = 'EPA PM10' + ' (#'+str(len(df.epa_lat))+')'
            epa_col = 'b'
            epa_mar = 'o'
            
            pur_lab = 'Purple PM10' + ' (#'+str(len(df.epa_lat))+')'
            pur_cpl = 'k'
            pur_mar = 'x'            


        ax.set_title('Location of EPA and Purple stations in '+ name )
        ax.scatter(x = df.epa_lon , y = df.epa_lat , s=15 , lw=1 , c= epa_col , marker = epa_mar, label = epa_lab , alpha=0.85)
        ax.scatter(x = df.p_lon   , y = df.p_lat   , s=15 , lw=1 , c= pur_col , marker = pur_mar, label = pur_lab , alpha=0.85)
        ax.legend(ncol=2)
        ax.legend()  
        ax.set_xlim(lim['xmin'],lim['xmax'])
        ax.set_ylim(lim['ymin'],lim['ymax'])
    
    plt.savefig(name+'_'+'all_stations.png',dpi=600)
    plt.close('all')













