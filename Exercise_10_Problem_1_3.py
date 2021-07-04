#!/usr/bin/env python
# coding: utf-8

# ## Problem 1: Geocode shopping centers
# 
# In problem 1 the task is to find out the addresses for a list of shopping centers and to geocode these addresses in order to represent them as points. The output should be stored in a Shapefile called `shopping_centers.shp` 
# 

# Import modules
import geopandas as gpd
import pandas as pd
# Read the data (replace "None" with your own code)
data = None
# YOUR CODE HERE 1 to read the data
 #read the txtfile&separate with ';'
data = pd.read_table('shopping_centers.txt', sep=';', header=None)
data.index.name = 'id'
data.columns=['name', 'addr']

#TEST CODE
# Check your input data
print(data)

# - Geocode the addresses using the Nominatim geocoding service. Store the output in a variable called `geo`:

# Geocode the addresses using Nominatim
geo = None
from geopandas.tools import geocode

# Geocode addresses using Nominatim. Remember to provide a custom "application name" in the user_agent parameter!
#YOUR CODE HERE 2 for geocoding
geo = geocode(data['addr'], provider='nominatim', user_agent='autogis_xx', timeout=4)

#TEST CODE
# Check the geocoded output
print(geo)

#TEST CODE
# Check the data type (should be a GeoDataFrame!)
print(type(geo))


# Check that the coordinate reference system of the geocoded result is correctly defined, and **reproject the layer into JGD2011** (EPSG:6668):

# YOUR CODE HERE 3 to set crs.
 #reproject the layer into JGD2011** (EPSG:6668)
from pyproj import CRS
geo = geo.to_crs(CRS.from_epsg(6668))

#TEST CODE
# Check layer crs
print(geo.crs)


# YOUR CODE HERE 4 to join the tables
geodata = geo.join(data)

#TEST CODE
# Check the join output
print(geodata.head())


# - Save the output as a Shapefile called `shopping_centers.shp` 

# Define output filepath
out_fp = None
# YOUR CODE HERE 5 to save the output
outfp = r"shopping_centers.shp"
 # Save to Shapefile
join = geo.join(data)
join.head()
join.to_file(outfp)
# TEST CODE
# Print info about output file
print("Geocoded output is stored in this file:", out_fp)


# ## Problem 2: Create buffegeodata['buffer']=Noners around shopping centers
# 
# Let's continue with our case study and calculate a 1.5 km buffer around the geocoded points. 
 

# YOUR CODE HERE 6 to create a new column
geodata['buffer']=None
# YOUR CODE HERE 7 to set buffer column
geodata.crs = CRS.from_epsg(32634).to_wkt()
geodata['buffer'] =geodata.buffer(1500)

#TEST CODE
print(geodata.head())

#TEST CODE
# Check the data type of the first value in the buffer-column
print(type(geodata.at[0,'buffer']))


#TEST CODE
# Check the areas of your buffers in km^2
print(round(gpd.GeoSeries(geodata["buffer"]).area / 1000000))


# - Replace the values in `geometry` column with the values of `buffer` column:

# YOUR CODE HERE 8 to replace the values in geometry
geodata['geometry'] = geodata['buffer']
#TEST CODE
print(geodata.head())


# ## Problem 3: How many people live near shopping centers? 
# 
# Last step in our analysis is to make a spatial join between our buffer layer and population data in order to find out **how many people live near each shopping center**. 
# 

# YOUR CODE HERE 9
# Read population grid data for 2018 into a variable `pop`. 
read_pop = r'data/500m_mesh_suikei_2018_shape_13/500m_mesh_2018_13.shp'
pop = gpd.read_file(read_pop)
# make two columns to select population
pop = pop[['PTN_2020', 'geometry']]
#TEST CODE
# Check your input data
print("Number of rows:", len(pop)) #5311
print(pop.head(3))


# In[ ]:


# Create a spatial join between grid layer and buffer layer. 
# YOUR CDOE HERE 10 for spatial join
pop.crs = CRS.from_epsg(32634).to_wkt()

# YOUR CODE HERE 11 to report how many people live within 1.5 km distance from each shopping center
join = gpd.sjoin(geodata, pop, how = 'inner', op = 'intersects')
grouped = join.groupby(['name'])
#I must install "rtree"& "geopandas" $"geopy"
#count the number of people
sum=0.0
for key, group in grouped:
  sum=round(group['PTN_2020'].sum())
print("the number of people who live within 1.5 km :", sum) #sum ⇒ 13732951

# **Reflections:**
#     
# - How challenging did you find problems 1-3 (on scale to 1-5), and why?
# - What was easy?
# - What was difficult?

# YOUR ANSWER HERE
"""
Challenging :5
It was hard for me, but I did my best.
I'm not sure the answer was correct or not, because there are many places "Tokyu store" and "National Azabu"  in Tokyo.
To report how many people live within 1.5 km distance from each shopping center in CODE11 was difficult.
"""
# Well done!
