# -*- coding: utf-8 -*-
"""Geospatial Analysis Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WEwOXneez2tl4XYfeQzRGNzMhCvTGhk1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read csv file
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Files/zomato.csv')

df.head()

# show the columns
df.columns

# show the datatype
df.dtypes

df.shape

# data cleaning
#find % of missing values in your data
#deal with missiong values

# findout missing data
df.isnull()

# sum of all missing data
df.isnull().sum()

# collect only those columns where data is missing
feature_na=[feature for feature in df.columns if df[feature].isnull().sum()>0]
feature_na

# % for find missing data
for feature in feature_na:
  print(' {} has {} missing values'.format(feature,np.round(df[feature].isnull().sum()/len(df)*100,4)))

df['rate'].unique()

#drop na 
df.dropna(axis='index',subset=['rate'],inplace=True)

df.shape

# drop /5
def split(x):
  return x.split('/')[0]

df['rate'] = df['rate'].apply(split)

df.head()

df['rate'].unique()

# replace new with 0
df.replace('NEW',0,inplace=True)

# replace - with 0
df.replace('-',0,inplace=True)

df['rate'].dtype

# convert object datatype to float
df['rate'] = df['rate'].astype(float)

df.head()

# analysis of average rating of restro
# groupby for name column
df.groupby('name')['rate'].mean()

df.groupby('name')['rate'].mean().to_frame()

df_rate = df.groupby('name')['rate'].mean().to_frame().reset_index()

# replace column name
df_rate.columns=['restaurant','avg_rating']
df_rate.head(20)

# get distribution of rating column and try to find out what distribution this feature support

# plot this using seaborn library
sns.displot(df_rate['avg_rating'])

# top restro chain in bengolore

df_rate.shape

# [0:20] it show top 20 restro and chains.index give the name of the restro
chains = df['name'].value_counts()[0:20]
sns.barplot(x=chains,y=chains.index)
plt.title('Most famous restro')
plt.xlabel('Number of outlets')

# find how many resto do not accept online orders

x= df['online_order'].value_counts()
x

labels1 = ['accepted','not accepted']

pip install plotly

import plotly.express as px

px.pie(df,values=x,labels=labels1,title='Pie Chart')

# ratio between restro that provides table and do not provide table

y=df['book_table'].value_counts()
y

labels2 = ['not book','book']

import plotly.graph_objs as go
from plotly.offline import iplot

# use textinfo for making % to value e.g 14.6% to 6433
trace= go.Pie(labels=labels2,values=y,hoverinfo='label+percent',textinfo='value')
iplot([trace])

# indepth analysis of types of restro we have

# find missing value
df['rest_type'].isna().sum()

# drop missing values
df['rest_type'].dropna(inplace=True)

#check any missing value is there or not
df['rest_type'].isna().sum()

len(df['rest_type'].unique())

trace1 = go.Bar(x=df['rest_type'].value_counts().nlargest(20).index,
    y=df['rest_type'].value_counts().nlargest(20)
)

iplot([trace1])

# analysis of highest voted restro

df.groupby('name')['votes'].sum().nlargest(20).plot.bar()

# using plotly
trace2 = go.Bar(x=df.groupby('name')['votes'].sum().nlargest(20).index,
                y=df.groupby('name')['votes'].sum().nlargest(20))

iplot([trace2])

# analysis of total restro at different locations of benglore

restaurant=[]
location=[]

for key,location_df in df.groupby('location'):
  location.append(key)
  restaurant.append(len(location_df['name'].unique()))

# create dataframe 
df_total=pd.DataFrame(zip(location,restaurant))
df_total

# give names to columns instead of 0 and 1
df_total.columns=['location','restaurant']
df_total

# show top  restro 
# in this case set index is used in which location set as a index
df_total.set_index('location',inplace=True)
df_total

df_total.sort_values(by='restaurant').tail(10)

df_total.sort_values(by='restaurant').tail(10).plot.bar()

# analysis of total variety of resto in benglore

cuisines = df['cuisines'].value_counts()[0:10]
cuisines

# plot this data

trace1 = go.Bar(
    x=df['cuisines'].value_counts()[0:10].index,
    y=df['cuisines'].value_counts()[0:10]
)

iplot([trace1])

# analyse approx cost of 2 people feature

df.columns

df['approx_cost(for two people)'].isna().sum()

# drop all missing value

df.dropna(axis='index',subset=['approx_cost(for two people)'],inplace=True)

df['approx_cost(for two people)'].isna().sum()

sns.distplot(df['approx_cost(for two people)'].isna().sum())

df['approx_cost(for two people)'].dtype

df['approx_cost(for two people)'].unique()

df['approx_cost(for two people)'] = df['approx_cost(for two people)'].apply(lambda x:x.replace(',',''))

df['approx_cost(for two people)'].unique()

df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(int)

df['approx_cost(for two people)'].dtype

sns.distplot(df['approx_cost(for two people)'])

# analyse 'approx cost of 2 people' vs 'rating'. find out some relationship

sns.scatterplot(x='rate',y='approx_cost(for two people)',data=df)

sns.scatterplot(x='rate',y='approx_cost(for two people)',hue='online_order',data=df)

# analyse is there any difference b/w votes of restro accepting and not accepting the online order

sns.boxplot(x='online_order',y='votes',data=df)

px.box(df,x='online_order',y='votes')

# analyse is there any difference b/w price of restro accepting and not accepting the online order

px.box(df,x='online_order',y='approx_cost(for two people)')

# most luxirious restro in banglore

df['approx_cost(for two people)'].min()

df['approx_cost(for two people)'].max()

df[df['approx_cost(for two people)']==6000]['name']

# analyse top 10 most expensive restro with approx cost for 2 people

data= df.copy()

data.set_index('name',inplace=True)

data.head()

data['approx_cost(for two people)'].nlargest(10).plot.bar()

# anayse of 10 cheap best restro

data['approx_cost(for two people)'].nsmallest(10).plot.bar()

# find all the restro that are below than 500 i.e. affordable

data[data['approx_cost(for two people)']<=500]

df_budget = data[data['approx_cost(for two people)']<=500].loc[:,('approx_cost(for two people)')]

df_budget.head()

df_budget = data[data['approx_cost(for two people)']<=500].loc[:,('approx_cost(for two people)')]
df_budget=df_budget.reset_index()
df_budget.head()

# analyse total restro that have good rating > 4 and that are budget too

df[(df['rate']>4) & (df['approx_cost(for two people)']<=500)].shape

df[(df['rate']>4) & (df['approx_cost(for two people)']<=500)]['name'].unique()

# analyse of total various affordable hotels at all locations of Bengolre

df_new = df[(df['rate']>4) & (df['approx_cost(for two people)']<=500)]

df_new.head()

location=[]
total=[]

for loc,location_df in df_new.groupby('location'):
  location.append(loc)
  total.append(len(location_df['name'].unique()))

location_df = pd.DataFrame(zip(location,total))

location_df.head()

location_df.columns=['location','restraurant']

location_df.head()

# find the best budget restro in any location

def return_budget(location,restaurant):
  budget = df[(df['approx_cost(for two people)']<400) & (df['location']==location) & (df['rate']>4) & (df['rest_type']==restaurant)]
  return(budget['name'].unique())

return_budget('BTM','Quick Bites')

# analyse the foodie areas

restautrant_location = df['location'].value_counts()[0:20]
sns.barplot(restautrant_location,restautrant_location.index)

# geographical analysis

# find latitudes and longitudes for each of the locations of Bengalore

# create new dataframe
locations = pd.DataFrame({'Name':df['location'].unique()})

locations.head()

# libarary for location analysis (for latitudes and longitudes)
!pip install geopy

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='app')

# np.nan handle the missing data
lat_lon=[]

for location in locations['Name']:
  location = geolocator.geocode(location)
  if location is None:
    lat_lon.append(np.nan)
  else:
    geo=(location.latitude,location.longitude)
    lat_lon.append(geo)

locations['geo_loc'] = lat_lon

locations.head()

#total number of locations
locations.shape

Rest_locations = pd.DataFrame(df['location'].value_counts().reset_index())

Rest_locations.head()

# change column name
Rest_locations.columns=['Name','Count']
Rest_locations.head()

Restaurant_locations = Rest_locations.merge(locations,on='Name',how='left').dropna()

Restaurant_locations.head()

# display in form of array
np.array(Restaurant_locations['geo_loc'])

# for unzip and it will return 2 tuple
lat,lon = zip(*np.array(Restaurant_locations['geo_loc']))

type(lat)

Restaurant_locations['lat']=lat
Restaurant_locations['lon']=lon

Restaurant_locations.head()

# to remove geo_lac column
Restaurant_locations.drop('geo_loc',axis=1,inplace=True)

Restaurant_locations.head()

# generate base map of Benglore

!pip install folium

import folium 
from folium.plugins import HeatMap

def generatebasemap(default_location=[12.97,77.59],default_zoom_start=12):
  basemap = folium.Map(location=default_location,zoom_start=default_zoom_start)
  return basemap

basemap = generatebasemap()

basemap

# heatmap of restraunt of benglore

# .values used for convert into array and .tolist() is used for convert into list
# add_to used for add basemap on heatmap

HeatMap(Restaurant_locations[['lat','lon','Count']].values.tolist(),max_zoom=20,radius=15).add_to(basemap)

basemap

# analyze the heatmap of north indian restraurant

df.head()

df2 = df[df['cuisines']=='North Indian']

df2.head()

north_india = df2.groupby(['location'],as_index=False)['url'].agg('count')

north_india.head()

# rename the column

north_india.columns = ['Name','count']

north_india.head()

north_india = north_india.merge(locations,on='Name',how='left').dropna()

north_india.head(10)

north_india['lat'],north_india['lon'] = zip(*north_india['geo_loc'].values)

north_india.head()

north_india.drop('geo_loc',axis=1,inplace=True)

north_india.head()

# .values used for convert into array and .tolist() is used for convert into list
# add_to used for add basemap on heatmap

basemap = generatebasemap()

HeatMap(north_india[['lat','lon','count']].values.tolist(),max_zoom=20,radius=15).add_to(basemap)


basemap

# analyze the which are the most popular casual dining restraurant chains?

df_1 = df.groupby(['rest_type','name']).agg('count')

df_1

df_1.sort_values(['url'],ascending=False)

df_1.sort_values(['url'],ascending=False).groupby(['rest_type'],as_index=False).apply(lambda x: x.sort_values(by='url',ascending=False))

df_1.sort_values(['url'],ascending=False).groupby(['rest_type'],as_index=False).apply(lambda x: x.sort_values(by='url',ascending=False))['url'].reset_index()

# rename url column to count
dataset = df_1.sort_values(['url'],ascending=False).groupby(['rest_type'],as_index=False).apply(lambda x: x.sort_values(by='url',ascending=False))['url'].reset_index().rename(columns={'url':'count'})

dataset

casual = dataset[dataset['rest_type']=='Casual Dining']

casual