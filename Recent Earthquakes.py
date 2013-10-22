# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Recent Earthquakes: Group 11

# <codecell>

import urllib
import json
import pandas as pd

url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson'
d = json.loads(urllib.urlopen(url).read())

data = pd.DataFrame(d.items())
data

# <codecell>

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
df[1:10]

# <codecell>

url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson'

import hashlib
from datetime import datetime

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
    filename = data_hash + "_" + date_str + ".geojson"
    urllib.urlretrieve(data_url, filename)
    print "data retrieved and saved as: " + filename

#save_live_data(url)

# <headingcell level=3>

# Plotting

# <codecell>

from mpl_toolkits.basemap import Basemap
from numpy import mean

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

# <codecell>

alaska = df[df['Src'] == 'ak']  ## THIS IS WORKING
plot_quakes(alaska)

# <codecell>


