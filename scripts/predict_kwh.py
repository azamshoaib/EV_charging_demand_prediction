import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split

def Pre_process_features(data):
    start=data['chargingHour'].min()
    end=data['chargingHour'].max()
    # calcuate unique number of time stamp
    data["chargingHour"]= pd.to_datetime(data["chargingHour"])
    new_data=data.set_index('chargingHour')
    charging_time=data['chargingHour'].unique()
    n_user=[]
    list_user=[]
    total_kwh=[]
    dayofweek=[]
    is_weekend=[]
    year=[]
    month=[]
    day=[]
    hour=[]
    dayofyear=[]
    weekofyear=[]
    temp=[]
    frost=[]
    humidity=[]
    rain=[]
    wind=[]

   

    for i in range(len(charging_time)):
        user_list=new_data.loc[charging_time[i]]['userID']
        if len(np.shape(user_list)) == 0:
            n_user.append(1)
            list_user.append(user_list)
            temp.append(new_data.loc[charging_time[i]]['temp'])
            frost.append(new_data.loc[charging_time[i]]['frost'])
            humidity.append(new_data.loc[charging_time[i]]['humidity'])
            rain.append(new_data.loc[charging_time[i]]['rain'])
            wind.append(new_data.loc[charging_time[i]]['wind'])
        else:    
            list_user.append(user_list.reset_index(drop=True))
            n_user.append(new_data.loc[charging_time[i]]['userID'].count())
            temp.append(new_data.loc[charging_time[i]]['temp'][0])
            frost.append(new_data.loc[charging_time[i]]['frost'][0])
            humidity.append(new_data.loc[charging_time[i]]['humidity'][0])
            rain.append(new_data.loc[charging_time[i]]['rain'][0])
            wind.append(new_data.loc[charging_time[i]]['wind'][0])
        total_kwh.append(new_data.loc[charging_time[i]]['kWhDelivered'].sum())
        dayofweek.append(charging_time[i].dayofweek)
        year.append(charging_time[i].year)
        month.append(charging_time[i].month)
        day.append(charging_time[i].day)
        hour.append(charging_time[i].hour)
        dayofyear.append(charging_time[i].dayofyear)
        weekofyear.append(charging_time[i].weekofyear)
        if charging_time[i].dayofweek >4:
            is_weekend.append(1)
        else:
            is_weekend.append(0)   


    y=total_kwh
    x=[n_user,dayofweek,year,month,day,hour,dayofyear,weekofyear,is_weekend,temp,frost,humidity,wind,rain]
    X=np.asarray(x).T
    Y=np.asarray(y)
    return Y,X


def predit(x,y):
    x_train, x_test, y_train, y_test = train_test_split(x ,y,test_size=0.3, random_state=42)
    model_reg = linear_model.LinearRegression()
    model_reg.fit(x_train,y_train)
    model_reg.score(x_test,y_test)


    Pred_Y= model_reg.predict(x_test)
    return Pred_Y

   


    




if __name__=='__main__':
    folder_path_data = '/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/'
    file_name = 'weather_processed_data.csv'
    data = pd.read_csv(folder_path_data+file_name,header=0)
    y,x=Pre_process_features(data)
    pred_y=predit(x,y)