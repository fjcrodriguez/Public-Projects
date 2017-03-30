import pandas as pd
import numpy as np
import sys


print "Crunching numbers, this might take less than a minute"

# Read in the data
# make sure the data is in same directory before continuing with the program
try:
    data = pd.read_csv('green_tripdata_2016-03.csv')
except:
    print "'green_tripdata_2016-03.csv' needs to be in the directory for this script to run"
    sys.exit()


# remove any points without gps coordinates. they are useless
data = data[ (data['Pickup_longitude'] != 0.0) & (data['Pickup_latitude'] != 0.0) ]
data = data[ (data['Dropoff_longitude'] != 0.0) & (data['Dropoff_latitude'] != 0.0) ]

temp = sys.stdout

sys.stdout = open('hw4_result.txt', 'w')
############# Question 1 ###################

print "Answer 1: Using only March data\n\n\n"


############# Question 2 ###################

# group vendorID's by longtitude and latitude - basically finds counts by gps coordinates
pickup_counts = data.groupby(['Pickup_longitude', 'Pickup_latitude'], as_index=False)['VendorID'].count()

# exclude the first value becuase the coordinates are zero
# which means the locations were missing when the data were collected
print 'Answer 2:\tTop 5 locations for pickups'
print pickup_counts.sort_values('VendorID', ascending=False)[1:6]
print '\n\n'



############ Question 3 ####################

# grouby gps coordinates of dropoff locations to get counts
dropoff_counts = data.groupby(['Dropoff_longitude', 'Dropoff_latitude'], as_index=False)['VendorID'].count()
dropoff_counts.columns = ['Dropoff_longitude', 'Dropoff_latitude', 'Counts']

# add percentage of total trips each location has
dropoff_counts['%ofTrips'] = dropoff_counts['Counts'] / float(dropoff_counts['Counts'].sum() )

# exclude the first value because the coordinates are zero
# which means the locations were missing when the data were collected
print 'Answer 3:\tTop 5 locations for dropoffs'
print dropoff_counts.sort_values('Counts', ascending=False)[1:6]
print '\n\n'



############ Question 4 #####################
data['lpep_pickup_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'])

# extract the hour from the pickup time stamp and create a column
data['pickup_hour'] = data['lpep_pickup_datetime'].apply(lambda x: x.hour)


# find the counts for each hour of the day
pickup_hour_counts = data.groupby('pickup_hour', as_index = False)['VendorID'].count()
pickup_hour_counts.columns = ['pickup_hour', 'Counts']

print 'Answer 4:\tTop 3 Hours to be picked up'
print pickup_hour_counts.sort_values('Counts', ascending=False)[:3]
print '\n\n'



############# Question 5 ##########################
data['Lpep_dropoff_datetime'] = pd.to_datetime(data['Lpep_dropoff_datetime'])

# create a column that is the duration of the trip in seconds 
data['duration'] = (data['Lpep_dropoff_datetime'] - data['lpep_pickup_datetime']).apply(lambda x: x.seconds)

# create a column for the Lucrative ratio (total amount of money / trip duration in seconds) 
data['duration_amount_ratio'] = data['Total_amount'] / data['duration']


# replace infinity values with NAs and then remove ovbservations with NAs
data = data.replace([np.inf, -np.inf], np.nan)
data = data[pd.notnull(data['duration_amount_ratio'])]

# use kmeans to group and separate high ratio and low ratio trips
from sklearn.cluster import KMeans

k = 2
km = KMeans(n_clusters=k)
km.fit(data.loc[:,'duration_amount_ratio'].reshape(-1,1))
data['class'] = km.labels_

grouped_classes = data.groupby('class', as_index=False)['duration_amount_ratio'].mean()

lucrative_class = int(grouped_classes.loc[ grouped_classes['duration_amount_ratio']== max(grouped_classes['duration_amount_ratio']), 'class'])
lucrative_trips = data[data['class']==lucrative_class]

pickup_countsL = lucrative_trips.groupby(['Pickup_longitude', 'Pickup_latitude'], as_index=False)['VendorID'].count()

print "Answer 5:\tTop 5 Pickup Locations by Lucrative Ratio"
print pickup_countsL.sort_values('VendorID', ascending=False).head()
print '\n\n'

############### Question 6 #########################
print "Answer 6:\tTop 5 Dropoff Locations by Lucrative Ratio"
dropoff_countsL = lucrative_trips.groupby(['Dropoff_longitude', 'Dropoff_latitude'], as_index=False)['VendorID'].count()
print dropoff_countsL.sort_values('VendorID', ascending=False).head()


sys.stdout = temp

print "results have been written to file, hw4_results.py"
