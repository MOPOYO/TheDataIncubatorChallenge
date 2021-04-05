import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# ##### 1. Start by considering just the data from 2020. Calls are classfied into several types. What fraction of calls are of the most common type?

# read the 2020 datafile
df_2020 = pd.read_csv("Call_for_Service_2020.csv", parse_dates = ["TimeCreate", "TimeDispatch", "TimeArrive", "TimeClosed"])
df_2020.head()

# check the column information
df_2020.info()

# count the number of different types and convert to a dataframe
df_2020["TypeText"].value_counts().to_frame(name = "counts")

# calculate the fraction of the most common type
fraction = df_2020["TypeText"].value_counts()[0]/len(df_2020)
print("{:.10f} of calls are of the most common type".format(fraction))


# ##### 2. Now compare to the data from 2016. Find the call type that displayed the largest percentage decrease in volume between 2016 and 2020. What is the fraction of the 2016 volume that this decrease represents? The answer should be between 0 and 1. (Note that the name of the type column changes over time. You can use the TypeText column, which remains constant, to determine the call type.)

# load the 2016 dataset
df_2016 = pd.read_csv("Calls_for_Service_2016.csv", parse_dates = ["TimeCreate", "TimeDispatch", "TimeArrive", "TimeClosed"])

# create two dataframes to store the counts of each type for each year
counts_2020 = df_2020["TypeText"].value_counts().to_frame(name = "counts_2020")
counts_2016 = df_2016["TypeText"].value_counts().to_frame(name = "counts_2016")

# merge the two dataframes
count_compare = counts_2016.merge(counts_2020, left_index = True, right_index = True)

# calculate the percentage changes from 2016 to 2020 and add one addtional column to store it
count_compare["change"] = (count_compare["counts_2016"] - count_compare["counts_2020"])/count_compare["counts_2016"]*100

# sort the percentage changes by descending order
count_compare.sort_values(by = ["change"], ascending = False)

# calculate the fraction of the type that is with the largest percenage decrease that represnts the 2016 volume
most_descrese  = count_compare.sort_values(by = ["change"], ascending = False).loc["WARR STOP WITH RELEASE", "counts_2016"]/len(df_2016)
print("WARR STOP WITH RELEASE has the largest percentage decrease between 2016 and 2020, and it represents {:.10f} fraction of the 2016 volume ".format(most_descrese))


# ##### 3. For this and the remaining questions, consider data from all five years. As you combine the data, you will notice that duplicate item numbers appear across years, for calls whose resolution spans the new year. Remove these duplicate rows. How many duplicate rows were removed?

# load 2017 dataset
df_2017 = pd.read_csv("Calls_for_Service_2017.csv", parse_dates = ["TimeCreate", "TimeDispatch", "TimeArrive", "TimeClosed"])

# load 2018 dataset
df_2018 = pd.read_csv("Calls_for_Service_2018.csv", parse_dates = ["TimeCreate", "TimeDispatch", "TimeArrive", "TimeClosed"])

# load 2019 dataset
df_2019 = pd.read_csv("Calls_for_Service_2019.csv", parse_dates = ["TimeCreate", "TimeDispatch", "TimeArrival", "TimeClosed"])

# reorder the 2019 dataset columns
df_2019 = df_2019[['NOPD_Item', 'Type', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrival', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location']]

# reorder the 2020 dataset columns
df_2020 = df_2020[['NOPD_Item', 'Type', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrive', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location']]

# rename of the 2019 dataset columns to be consistent
df_2019.columns = ['NOPD_Item', 'Type_', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrive', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location']

# rename of the 2020 dataset columns to be consistent
df_2020.columns = ['NOPD_Item', 'Type_', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrive', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location']

# concatenate the 2016, 2017, 2018, 2019, 2020 datasets
frames = [df_2016, df_2017, df_2018, df_2019, df_2020]
df_all = pd.concat(frames)

# find the duplicate records based on NOPD_Items and count the number
dup_item = df_all.duplicated(subset = ["NOPD_Item"]).sum()

# remove all duplicated records and only keeps the first occurance. 
df_all = df_all.drop_duplicates(subset = "NOPD_Item", keep = "first")

print("{} duplicate rows were removed!".format(dup_item))


# ##### 4. Some calls result in an officer being dispatched to the scene, and some log an arrival time. What is the median response time (dispatch to arrival), in seconds, considering only valid (i.e. non-negative) times?

# confirm that the TimeDispatch and TimeArrive columsn are datetime type
df_all.info()

# calculate the time difference between arrival and dispatch in seconds
deltas = (df_all["TimeArrive"] - df_all["TimeDispatch"]).dt.seconds

# filter out negative numbers and NaT, and calculate the median
median_response = deltas[deltas >=0].median()

print("The median response time (dispatch to arrival) is {:.10f} seconds".format(median_response))


# ##### 5. Work out the average (mean) response time in each district. What is the difference between the average response times of the districts with the longest and shortest times?

# add one columns for the reponse times
df_all["response"] = (df_all["TimeArrive"] - df_all["TimeDispatch"]).dt.seconds

# create a new dataframe to only contain the recoreds with valid response time.
df_all_valid = df_all[df_all["response"] >= 0]

# calculate the average response of different police districts and sort the values
df_all_valid.groupby("PoliceDistrict")["response"].mean().sort_values()

# calculatge the difference between the average response times of the districts with the longest and shortest times
response_difference = df_all_valid.groupby("PoliceDistrict")["response"].mean().max() - df_all_valid.groupby("PoliceDistrict")["response"].mean().min()

print("Difference between the average response times of the districts with the longest and shortest times is {:.10f} seconds".format(response_difference))


# ##### 6. Work out the average response time for each month. Make an ordinary least-squares fit to the response time against month. What is the slope of this line, in seconds per year?

# Use the dataframe with valid response time, and one column for year and one column for month
df_all_valid["year"] = df_all_valid["TimeDispatch"].dt.year
df_all_valid["month"] = df_all_valid["TimeDispatch"].dt.month

# for each year in the datasets, find average response time for each month, concate to a new dataframe, and run ordinary least-sqaures.
df_ols = pd.DataFrame()
for yr in [2016, 2017, 2018, 2019, 2020]:
    df_lr = df_all_valid[df_all_valid["year"] == yr]
    df_ols = pd.concat([df_ols, df_lr.groupby("month")["response"].mean().to_frame().reset_index()])
    
# calculate the coefficient of OLS using np.polyfit
coefficient, intercept = np.polyfit(df_ols["month"], df_ols["response"], deg = 1)

print("The slope of this line, in seconds per year to fit to the response time against month is {:.10f}".format(coefficient))


# ##### 7. We can define surprising event types as those that occur more often in a district than they do over the whole city. What is the largest ratio of the conditional probability of an event type given a district to the unconditional probability of that event type? Consider only events types which have more than 100 events. Note that some events have their locations anonymized and are reported as being in district "0". These should be ignored.

# filter out the records that are reported as being in district "0"
df_events = df_all[df_all["PoliceDistrict"] != 0]

# create a dataframe to count the number of occurances of each type, sort and find the ones have more than 100 events
df_counts = df_events.groupby("TypeText")["NOPD_Item"].count().sort_values().to_frame(name = "Count").reset_index()

# filter the type that have less than 100 events. 
df_counts = df_counts[df_counts["Count"] > 100]

# use the identifed TypeText to get all recoreds that are with the type having more than 100 events. 
df_events = df_events[df_events["TypeText"].isin(set(df_counts["TypeText"]))]

# calculate the probailbity of events in each district
district_probs = df_events.groupby("PoliceDistrict").size().div(len(df_events))

# calculate the conditional probablity for each event type given a distrct 
df_condtional = df_events.groupby(["TypeText", "PoliceDistrict"]).size().div(len(df_events)).div(district_probs, axis = 0, level = "PoliceDistrict").to_frame()

# calculate the probailbity of events in each type
type_probs = df_events.groupby("TypeText").size().div(len(df_events))

# calculate the ratio of the conditional probability of an event type given a district to the unconditional probability of that event type
df_ratio = df_condtional.div(type_probs, axis = 0, level = "TypeText")

print("the largest ratio of the conditional probability of an event type given a district to the unconditional probability of that event type is {:.10f}".format(df_ratio.max()[0]))


# ##### 8.We can use the call locations to estimate the areas of the police districts. Represent each as an ellipse with semi-axes given by a single standard deviation of the longitude and latitude. What is the area, in square kilometers, of the largest district measured in this manner?

# The Location column need some preprocessing. This time we reload all datasets but do not need convert datetime to save computation time
df_2020_area = pd.read_csv("Call_for_Service_2020.csv")
df_2019_area = pd.read_csv("Calls_for_Service_2019.csv")
df_2018_area = pd.read_csv("Calls_for_Service_2018.csv")
df_2017_area = pd.read_csv("Calls_for_Service_2017.csv")
df_2016_area = pd.read_csv("Calls_for_Service_2016.csv")

#add two columns for 2020 data for latitude and longitude 
lon_2020 = []
lat_2020 = []

for index, row in df_2020_area.iterrows():
    lon_2020.append(df_2020_area.Location[index].split("(")[1].rstrip(")").split(" ")[0])
    lat_2020.append(df_2020_area.Location[index].split("(")[1].rstrip(")").split(" ")[1])

df_2020_area["lon"] = lon_2020
df_2020_area["lat"] = lat_2020

# add two columns for 2019 data for latitude and longitude 
lon_2019 = []
lat_2019 = []
index_2019 = []
df_2019_area["Location"].fillna("(0.0, 0.0)", inplace = True)

# add two columns for 2019 data fro latitude and longitude
for index, row in df_2019_area.iterrows():
    try:
        lon_2019.append(df_2019_area.Location[index].split("(")[1].rstrip(")").split(", ")[1])
        lat_2019.append(df_2019_area.Location[index].split("(")[1].rstrip(")").split(", ")[0])
        index_2019.append(index)
    except:
        print(index, "error")

df_2019_area = df_2019_area.loc[index_2019]
df_2019_area["lon"] = lon_2019
df_2019_area["lat"] = lat_2019

# add two columns for 2018 data for latitude and longitude 
lon_2018 = []
lat_2018 = []
index_2018 = []
df_2018_area["Location"].fillna("(0.0, 0.0)", inplace = True)

# add two columns for 2018 data fro latitude and longitude
for index, row in df_2018_area.iterrows():
    try:
        lon_2018.append(df_2018_area.Location[index].split("(")[1].rstrip(")").split(", ")[1])
        lat_2018.append(df_2018_area.Location[index].split("(")[1].rstrip(")").split(", ")[0])
        index_2018.append(index)
    except:
        print(index, "error")

df_2018_area = df_2018_area.loc[index_2018]
df_2018_area["lon"] = lon_2018
df_2018_area["lat"] = lat_2018

# add two columns for 2017 data for latitude and longitude 
lon_2017 = []
lat_2017 = []
index_2017 = []
df_2017_area["Location"].fillna("(0.0, 0.0)", inplace = True)

# add two columns for 2017 data fro latitude and longitude
for index, row in df_2017_area.iterrows():
    try:
        lon_2017.append(df_2017_area.Location[index].split("(")[1].rstrip(")").split(", ")[1])
        lat_2017.append(df_2017_area.Location[index].split("(")[1].rstrip(")").split(", ")[0])
        index_2017.append(index)
    except:
        print(index, "error")

df_2017_area = df_2017_area.loc[index_2017]
df_2017_area["lon"] = lon_2017
df_2017_area["lat"] = lat_2017

# add two columns for 2016 data for latitude and longitude 
lon_2016 = []
lat_2016 = []
index_2016 = []
df_2016_area["Location"].fillna("(0.0, 0.0)", inplace = True)

# add two columns for 2016 data fro latitude and longitude
for index, row in df_2016_area.iterrows():
    try:
        lon_2016.append(df_2016_area.Location[index].split("(")[1].rstrip(")").split(", ")[1])
        lat_2016.append(df_2016_area.Location[index].split("(")[1].rstrip(")").split(", ")[0])
        index_2016.append(index)
    except:
        print(index, "error")

df_2016_area = df_2016_area.loc[index_2016]
df_2016_area["lon"] = lon_2016
df_2016_area["lat"] = lat_2016

# reorder the 2019 and 2020 column names to be consistent
df_2019_area = df_2019_area[['NOPD_Item', 'Type', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrival', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location', "lon", "lat"]]

df_2020_area = df_2020_area[['NOPD_Item', 'Type', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrive', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location',"lon", "lat"]]

# rename the 2019 and 2020 column names to be consistent
df_2019_area.columns = ['NOPD_Item', 'Type_', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrive', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location',"lon", "lat"]
df_2020_area.columns = ['NOPD_Item', 'Type_', 'TypeText', 'Priority', 'InitialType',
       'InitialTypeText', 'InitialPriority', 'MapX', 'MapY', 'TimeCreate',
       'TimeDispatch', 'TimeArrive', 'TimeClosed', 'Disposition',
       'DispositionText', 'SelfInitiated', 'Beat', 'BLOCK_ADDRESS', 'Zip',
       'PoliceDistrict', 'Location', "lon", "lat"]

# concatenate the dataframes of all five years and remove the duplicated records based on NOPD_Item
frames_area = [df_2016_area, df_2017_area, df_2018_area, df_2019_area, df_2020_area]
df_area = pd.concat(frames_area)
df_area = df_area.drop_duplicates(subset = "NOPD_Item", keep = "first")

# convert lon and lat to float datatype
df_area["lon"] = df_area["lon"].astype(float)
df_area["lat"] = df_area["lat"].astype(float)

# remove the records with missing or ambigious (e.g., 0.0, 0.0) lon and lat information (some bad lon/lat data have been removed)
df_area = df_area[(df_area["lon"] != 0) & (df_area["lat"] != 0)]

# Based on the simple calculation to covert latitude and longitude to kilometer
# Latitude: 1 deg = 110.574 km. Longitude: 1 deg = 111.320*cos(latitude) km.

# convert latitude to kilometer
df_area["lat_kilo"] = df_area["lat"] * 110.574

# convert longitude to kilomters (need to caculate the cosine of radians of latitude first)
df_area["lat_cos"] = df_area["lat"].apply(math.radians).apply(math.cos)
df_area["lon_kilo"] = df_area["lat_cos"] * df_area["lon"] * 111.320

# groupby different policy district and find the standard deviation in kilometers as semi-axes
district_area = df_area[df_area["PoliceDistrict"]!=0].groupby("PoliceDistrict")[["lat_kilo", "lon_kilo"]].std()

# calculate the ellipse area for each police distrct and find the largest
district_area["area"] = district_area['lat_kilo'] * district_area["lon_kilo"] * math.pi
district_area.sort_values("area", ascending = False)

print("the largest district is {:.10f} square kilometers".format(district_area.area.max()))



