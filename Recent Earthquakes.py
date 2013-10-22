# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Recent Earthquakes: Group 11
# This is Group11's submission of [this Stat157 assignment](https://github.com/stat157/recent-quakes).
# 
# To ignore the code details and just plot the most recent quakes in northern california, scroll to the bottom.
# 
# To specify options (like using cached data), read on!

# <markdowncell>

# ##Data Curation
# 
# Options for how to plot earthquakes:
# 
# + Live data [optionally, save it locally]
# + Cached Data

# <markdowncell>

# ### Specify program options
# 
# First, specify whether the data should be stored locally.  Optionally specify a filename.

# <codecell>

use_live_data = True
# To use cached data, set use_live_data to False.  

# If you use cached data, you can optionally specify a different filename below:
filename = 'data/f8c7029ef946b7df10fca0fb4908d7f1c3dedd91_2013-10-22_0354.geojson'

caching = False
# To store the data locally, set caching to True

region = 'nc'
# region must be a valid USGS network contributor: try nc, ak, ci

# <markdowncell>

# Next, you can specify the URL from which to retrieve the data.  The list of USGS earthquake data feeds is [here](https://github.com/reenashah/recent-quakes-Group11-data).
# 
# If you're using cached data, ignore this.

# <codecell>

url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson'
# You can modify this URL to use any USGS earthquake feed
# The list of feeds is located at: 
# http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

# <markdowncell>

# Import the necessary libraries.

# <codecell>

import urllib
import json
import pandas as pd
import hashlib
from datetime import datetime

# <markdowncell>

# ### Cache the Live Data
# This function uses the live data fetched from the URL above and saves it in a directory named `data/`.
# 
# The filename contains the current datetime and a SHA-1 hash of the data, so you can easily recognize whether data sources are identical.
# 
# To cache this locally-saved data in [our data repository](https://github.com/reenashah/recent-quakes-Group11-data), submit a pull request!

# <codecell>

def save_live_data(data_url):
    """
    Fetches the data from DATA_URL and saves it.
    The filename is of the format: <HASH>_<DATE>_<TIME>.geojson,
        where <HASH> is a SHA1 hash of the file at data_url,
        <DATE> and <TIME> are the current UTC date and time.

    DATA_URL: a string containing the URL of geojson data, e.g. 
              'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson'
    """
    
    data = urllib.urlopen(data_url).read()
    data_hash = hashlib.sha1(data).hexdigest()
    date_str = datetime.utcnow().strftime("%Y-%m-%d_%H%M")
    filename = "data/" + data_hash + "_" + date_str + ".geojson"
    urllib.urlretrieve(data_url, filename)
    print "data retrieved and saved as: " + filename

# <markdowncell>

# ### Turn JSON data into a useful data frame
# 
# This section is the meat of the curation: it extracts the JSON data from the URL above, formats it into a Python-Pandas DataFrame.

# <codecell>

def process_json_data(data):
    """
    Returns a Pandas DataFrame containing relevant quake information.

    DATA: A Pandas DataFrame object, produced by plot_data.  
    [1,1] should contain the relevant JSON data.
    """
    
    features = data[1].values[1]
    
    Latitude = []    
    Longitude = []   
    Depth = []    
    Magnitude = []    
    Place = []
    Time = []
    Source = []
    Eqid = []
    Nst = []
    
    for item in features:
        geometry = item['geometry']
        properties = item['properties']
        Longitude.append(geometry['coordinates'][0])
        Latitude.append(geometry['coordinates'][1])
        Depth.append(geometry['coordinates'][2])
        Source.append(properties['net'])
        Eqid.append(properties['code'])
        Place.append(properties['place'])
        Nst.append(properties['nst'])
        Time.append(properties['time'])
        Magnitude.append(properties['mag'])
    
    allQuakes = {
                'Src': Source, 
                'Eqid': Eqid,
                'Datetime': Time,
                'Place': Place, 
                'NST': Nst, 
                'Lat': Latitude, 
                'Lon': Longitude, 
                'Depth': Depth,
                'Magnitude': Magnitude
                }

    df = pd.DataFrame.from_dict(allQuakes)
    return df

# <headingcell level=3>

# Plotting

# <codecell>

from mpl_toolkits.basemap import Basemap

def plot_quakes(quakes):
    """
    Plots earthquakes (specified in QUAKES) as slightly-transparent
    orange circles with area proportional to magnitude and 
    color indicating depth.

    QUAKES: a Pandas DataFrame object containing earthquake data
            with parameters "Lat", "Lon", "Magnitude"
    """
    
    heatcolors = ('#FFFF00','#FF9900','#CC3333')
    heatcolor = None
                   
    cenlat = quakes['Lat'].mean()
    cenlon = quakes['Lon'].mean()
    fig = matplotlib.pyplot.figure(figsize=(9,9))
    m = Basemap(resolution = 'l', projection='nsper',
                area_thresh = 1000., satellite_height = 200000,
                lat_0 = cenlat, lon_0 = cenlon)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color = '#0CAA43', lake_color = 'aqua')
    m.drawmapboundary(fill_color = '#0B5BD2')
    x, y = m(quakes.Lon, quakes.Lat)
    for i in range(0, len(x) - 1):
        if quakes.Depth[i:i+1] < 70:
            heatcolor = heatcolors[1]
        elif 70 <= quakes.Depth[i:i+1] < 300:
            heatcolor = heatcolors[2]
        else:
            heatcolor = heatcolors[3]
        m.plot(x[i:i+1], y[i:i+1], heatcolor, 
               marker = 'o', markersize = (pi*quakes.Magnitude[i:i+1]**2), 
               alpha = 0.6)
    return m

# <markdowncell>

# ### Main Function

# <codecell>

def plot_data(caching=False, use_live_data=True, region='nc',
              url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson', 
              filename='data/f8c7029ef946b7df10fca0fb4908d7f1c3dedd91_2013-10-22_0354.geojson'):
    """
    CACHING: If true, saves the data locally.  Will not save unless USE_LIVE_DATA is True.
    USE_LIVE_DATA: if true, uses live USGS data fetched from URL.
                   if false, uses cached data from FILENAME.
    """
    
    if (use_live_data):
        data_source = urllib.urlopen(url).read()
        if (caching):
            save_live_data(url)
    else:
        f = open(filename, mode='r')
        data_source = f.read()
    
    d = json.loads(data_source)
    data = pd.DataFrame(d.items())

    df = process_json_data(data)
    df_subset = df[df['Src'] == region]
    
    plot_quakes(df_subset)
    

# <markdowncell>

# # Final Product

# <codecell>

plot_data(caching, use_live_data, region, url, filename)

