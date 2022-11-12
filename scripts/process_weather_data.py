import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd



# To extract features using raw data in csv
def data_preprocess(data_caltech):
    newData = []
    for i in range(len(data_caltech)):
        # print('---------------------------------------------')
        data_to_insert = []
        item = data_caltech.iloc[i]
        start = item['ConnectionTime']
        end = item['DoneCharging']
        kWhDelivered = item['kWhDelivered']
        userID = item['userID']

        # total difference between starting and ending time
        difference = end - start
        difference_seconds = difference.total_seconds()

        # if total difference in seconds is less than 0 , it means data is corrupt
        if (difference_seconds > 0 ):
            
            # absolute hour of starting and ending time and corresponding data 
            start_H = item['ConnectionTime'].replace(minute=0, second=0)
            end_H = item['DoneCharging'].replace(minute=0, second=0)  

            absolute_hours_bw = (end_H - start_H)  / np.timedelta64(1, 'h')  - 1     
            absolute_seconds_per_hour = 3600

            if (absolute_hours_bw >=0):

        
                seconds_in_first_part = 3600 - (start - start_H).total_seconds()
                seconds_in_second_part = (end - end_H).total_seconds()
                
                # kWhDelivered in three sections
                kWhDelivered_in_first_part = (seconds_in_first_part/difference_seconds) * kWhDelivered
                kWhDelivered_in_second_part = (seconds_in_second_part/difference_seconds) * kWhDelivered
                kWhDelivered_in_absolute_part = (absolute_seconds_per_hour/difference_seconds) * kWhDelivered

                # first part appended
                data_to_insert.append([start_H,kWhDelivered_in_first_part,userID])
                

                # looping for absolute parts
                for j in range(int(absolute_hours_bw)):
                    start_H = start_H + pd.Timedelta(hours=1)
                    data_to_insert.append([start_H,kWhDelivered_in_absolute_part,userID])

                # second part appended
                data_to_insert.append([end_H,kWhDelivered_in_second_part,userID])
                
            # full kwhdelivered to same hour
            else:
                data_to_insert.append([start_H,kWhDelivered,userID])
            newData += data_to_insert
    new_feature_data = pd.DataFrame(newData)
    new_feature_data.columns = ['chargingHour','kWhDelivered','userID']
    # new_feature_data = new_feature_data.set_index('chargingHour')
    return new_feature_data


# process the raw data downloaded from the NASA website, It changes the date and time format to %y%M%D%H%%M%S 
def data_preprocess_weather(data_weather):
   
    date_time=[]
    temp=[]
    frost=[]
    humidity=[]
    rain=[]
    wind=[]

    for i in range(len(data_weather)):
        date_time.append(pd.Timestamp(data_weather['YEAR'].iloc[i],data_weather['MO'].iloc[i],data_weather['DY'].iloc[i],data_weather['HR'].iloc[i]))
        temp.append(data_weather['T2M'].iloc[i])
        frost.append(data_weather['T2MDEW'].iloc[i])
        humidity.append(data_weather['QV2M'].iloc[i])
        rain.append(data_weather['PRECTOTCORR'].iloc[i])
        wind.append(data_weather['WS2M'].iloc[i])

    data = {'date_time':date_time, 'temp':temp,'frost':frost,'humidity':humidity,'rain':rain,'wind':wind}  
    new_data_weather = pd.DataFrame(data)  
    # new_data_weather=pd.DataFrame([date_time,temp,frost,humidity,rain,wind])
    # new_data_weather.columns = ['date_time','temp','frost','humidity','rain','wind']

    return new_data_weather


# to find the the date and time in weather data and add the weather information to ACN data    
def combine_data(data,data_weather):
 
    data1=data_weather.set_index('date_time')
    weather=[]
    combined_features=[]
    for i in range(len(data)):
        aa=data1.loc[data['chargingHour'].iloc[i]]
        combined_features.append([data['chargingHour'].iloc[i],data['kWhDelivered'].iloc[i],data['userID'].iloc[i],aa['temp'],aa['frost'],aa['humidity'],aa['rain'],aa['wind']])
    
    # data = {'date_time':date_time, 'temp':temp,'frost':frost,'humidity':humidity,'rain':rain,'wind':wind}  
    new_combined_features = pd.DataFrame(combined_features) 
    new_combined_features.columns = ['chargingHour','kWhDelivered','userID','temp','frost','humidity','rain','wind']

    return new_combined_features




if __name__=='__main__':
    folder_path_data = '/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/'
    file_name = 'charging_office_clean.csv'
    weather_file_name = 'office_weather.csv'
    processed_data_file = 'processed_data.csv'
    new_data_file='weather_processed_data.csv'
    
    # read the raw data
    data = pd.read_csv(folder_path_data+file_name,header=0, parse_dates=[2,3],usecols=[3,9,10,12])
    processed_data = data_preprocess(data)
    processed_data.to_csv(folder_path_data+processed_data_file)


    # data = pd.read_csv(folder_path_data+processed_data_file)
    # read the weather data 
    data_weather = pd.read_csv(folder_path_data+weather_file_name)
    processed_data_weather = data_preprocess_weather(data_weather)
    processed_data_combined = combine_data(processed_data,processed_data_weather)
    processed_data_combined.to_csv(folder_path_data+new_data_file)
    # charging_demand_day = charging_demand_per_day(processed_data)
    # charging_demand_hour = charging_demand_per_hour(processed_data)
    # charging_demand_day.to_csv(folder_path_data+charging_demand_day_file)
    # charging_demand_hour.to_csv(folder_path_data+charging_demand_hour_file)
    print('processed_data.csv, charging_demand_hour.csv, charging_demand_day.csv and plots for charging demand are created.')
