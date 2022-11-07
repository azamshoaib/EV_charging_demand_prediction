import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd


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
    new_feature_data = new_feature_data.set_index('chargingHour')

    return new_feature_data

def charging_demand_per_hour(processed_data):
    df_hour = processed_data.groupby(['chargingHour']).sum()
    plt.figure(dpi=1200)
    plt.plot(df_hour.index, df_hour['kWhDelivered'], label='original',linewidth=1)
    plt.gcf().autofmt_xdate()
    plt.title('Hour Wise on Caltech Dataset ')
    plt.xlabel('Date')
    plt.ylabel('Energy Delivered (in KWh)')
    plt.savefig('Hourwise.png', dpi=1200)
    return df_hour

def charging_demand_per_day(processed_data):
    df_day = processed_data.resample('D').sum()
    plt.figure(dpi=1200)
    plt.plot(df_day.index, df_day['kWhDelivered'],label='original',linewidth=1)
    plt.gcf().autofmt_xdate()
    plt.title('Day Wise on Caltech Dataset')
    plt.xlabel('Date')
    plt.ylabel('Energy Delivered (in KWh)')
    plt.savefig('Daywise.png', dpi=1200)
    return df_day


if __name__=='__main__':
    folder_path_data = '/home/shoaib/work/acn/scripts/'
    file_name = 'charging_caltech_clean.csv'
    processed_data_file = 'processed_data.csv'
    charging_demand_day_file = 'charging_demand_day.csv'
    charging_demand_hour_file = 'charging_demand_hour.csv'
    data = pd.read_csv(folder_path_data+file_name,header=0, parse_dates=[2,3],usecols=[3,9,10,12])
    processed_data = data_preprocess(data)
    processed_data.to_csv(folder_path_data+processed_data_file)
    charging_demand_day = charging_demand_per_day(processed_data)
    charging_demand_hour = charging_demand_per_hour(processed_data)
    charging_demand_day.to_csv(folder_path_data+charging_demand_day_file)
    charging_demand_hour.to_csv(folder_path_data+charging_demand_hour_file)
    print('processed_data.csv, charging_demand_hour.csv, charging_demand_day.csv and plots for charging demand are created.')
