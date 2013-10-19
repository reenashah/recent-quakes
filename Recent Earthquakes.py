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

# <markdowncell>

# Now let's just focus on earthquakes in Alaska (my home state! :)

# <codecell>

alaska = clean_data[clean_data.Src == 'ak']
alaska[0:10]

# <codecell>

from mpl_toolkits.basemap import Basemap

def plot_quakes(quakes):
    m = Basemap(llcrnrlon=-180,llcrnrlat=50.,
                urcrnrlon=-120.,urcrnrlat=72,
                resolution='l',area_thresh=1000.,projection='merc',
                lat_0=62.9540,lon_0=-149.2697)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral',lake_color='blue')
    m.drawmapboundary(fill_color='aqua')
    x, y = m(quakes.Lon, quakes.Lat)
    m.plot(x, y, 'k.')
    return m

plot_quakes(alaska)

# <codecell>

import urllib
import json
import pandas as pd

url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson'
d = json.loads(urllib.urlopen(url).read())

data = pd.DataFrame(d.items())
data

# <codecell>

alaska = clean_data[clean_data.Src == 'ak']

clean_data.Src
unique(clean_data.Src)

# <codecell>

from mpl_toolkits.basemap import Basemap

def plot_quakes(quakes):
    cenlat = sum(quakes.Lat)/len(quakes.Lat)
    cenlon = sum(quakes.Lon)/len(quakes.Lon)
    m = Basemap(resolution='l',projection='nsper',area_thresh=1000., satellite_height=200000,
        lat_0=cenlat,lon_0=cenlon)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color='coral',lake_color='blue')
    m.drawmapboundary(fill_color='aqua')
    x, y = m(quakes.Lon, quakes.Lat)
    for i in range(0,len(x)-1):
        m.plot(x[i:i+1], y[i:i+1], 'g',marker='o',markersize=(pi/2*quakes.Magnitude[i:i+1]**2),alpha=0.6)
    return m

# <codecell>

plot_quakes(alaska)

# <codecell>

unique(clean_data.Src)

# <codecell>

x = clean_data[clean_data.Src == 'uu']
plot_quakes(x)

# <codecell>

# Reverse Geocoding Testing
from pygeocoder import Geocoder

results = Geocoder.reverse_geocode(60.2912, -150.7650)
results.state

# <codecell>

x[0:4]

# <codecell>


