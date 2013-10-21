# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Use [urllib](http://docs.python.org/2/library/urllib.html) to open arbitrary resources by URL and pass that data to the [read_csv](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.io.parsers.read_csv.html) function of pandas. Then print out the first few rows of data using pandas [Indexing and Selecting Data](http://pandas.pydata.org/pandas-docs/dev/indexing.html).

# <codecell>

import urllib
from pandas import read_csv


url = 'http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M1.txt'
data = read_csv(urllib.urlopen(url))

data[0:10]

# <markdowncell>

# **UH OH!** Note that our data is a bit *dirty* and contains a notice that this data feed has been deprecated:

# <codecell>

print data[0:1]['Src'].values[0]

# <markdowncell>

# We can filter out the dirty data using [dropna](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.dropna.html) to drop any rows that contain **NaN**.

# <codecell>

clean_data = data.dropna(axis=0, how='any')
clean_data[0:3]

# <markdowncell>

# In the code above note that I saved the results of `data.dropna()` into a different variable `clean_data` rather than over-writing the old variable `data`. **Why?** Why not just re-use old variable names? And if we did re-use old variable names what extra danger do we have to keep in mind while using the IPython Notebook?

# <codecell>

import urllib
import json
import pandas as pd
from pprint import pprint

url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
quakes = json.loads(urllib.urlopen(url).read())
data = pd.DataFrame(d.items())
features = data[1].values[1]
pprint(features)

# <codecell>

longitudedata = [];
for i in range(0,len(quakes['features'])):
    longitudedata.append(quakes['features'][i]['geometry']['coordinates'][0])

print longitudedata

# <codecell>

latitudedata = [];
for i in range(0,len(quakes['features'])):
    latitudedata.append(quakes['features'][i]['geometry']['coordinates'][1])

print latitudedata

# <codecell>

altitudedata = [];
for i in range(0,len(quakes['features'])):
    altitudedata.append(quakes['features'][i]['geometry']['coordinates'][2])

print altitudedata

# <codecell>

sourcedata = [];
for i in range(0,len(quakes['features'])):
    sourcedata.append(quakes['features'][i]['properties']['net'])

print sourcedata

# <codecell>

equidata = [];
for i in range(0,len(quakes['features'])):
    equidata.append(quakes['features'][i]['properties']['code'])

print equidata

# <codecell>

timedata = [];
for i in range(0,len(quakes['features'])):
    timedata.append(quakes['features'][i]['properties']['time'])

timedata = pd.to_datetime(pd.Series(timedata))

print timedata

# <codecell>

nstdata = [];
for i in range(0,len(quakes['features'])):
    nstdata.append(quakes['features'][i]['properties']['nst'])

print nstdata

# <codecell>

placedata = [];
for i in range(0,len(quakes['features'])):
    placedata.append(quakes['features'][i]['properties']['place'])

print placedata

# <codecell>

magdata = [];
for i in range(0,len(quakes['features'])):
    magdata.append(quakes['features'][i]['properties']['mag'])

print magdata

# <codecell>

updateddata = [];
for i in range(0,len(quakes['features'])):
    updateddata.append(quakes['features'][i]['properties']['updated'])
    
updateddata = pd.to_datetime(pd.Series(updateddata))

print updateddata

# <codecell>

dict = {'Longitude': longitudedata,
'Latitude': latitudedata,
'Altitude': altitudedata,
'Datetime': timedata,
'Region': placedata,
'Magnitude': magdata,
'Source': sourcedata,
'Nst': nstdata,
'Eqid': equidata,
'Updated':updateddata
}
print dict

# <codecell>

import pandas as pd
pd.DataFrame.from_dict(dict)[0:4]

# <markdowncell>

# Now let's just focus on earthquakes in Alaska (my home state! :)

# <codecell>

alaska = clean_data[clean_data.Src == 'ak']
alaska[0:10]

# <codecell>

from mpl_toolkits.basemap import Basemap
from numpy import mean

def plot_quakes(quakes):
    """
    Plots earthquakes (specified in QUAKES) as slightly-transparent
    orange circles with area proportional to magnitude.

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
        if quakes.Depth[i:i+1]<70:
            heatcolor = heatcolors[1]
        elif 70<=quakes.Depth[i:i+1]<300:
            heatcolor = heatcolors[2]
        else:
            heatcolor = heatcolors[3]
        m.plot(x[i:i+1], y[i:i+1], heatcolor, 
               marker = 'o', markersize = (pi*quakes.Magnitude[i:i+1]**2), 
               alpha = 0.6)
    return m

plot_quakes(alaska)

# <codecell>


