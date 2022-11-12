import json
import pandas as pd



# data_path='/media/farzeen/sabrent/sabent/Engergy/acndata_sessions.json'
# f = open(data_path)
# data = json.load(f)
# f.close()
# df=pd.DataFrame(data["_items"])


def get_data(file_path=''):
    '''
    Reads .json file.
    Breaks data into two tables - charging and users.
    Saves tables as .csv.
    '''
    f = open(file_path)
    data = json.load(f)
    f.close()
    df=pd.DataFrame(data["_items"])
    # df = pd.json_normalize(data['_items'], record_path =['students'])
    
    # creating a table with information about charging sessions
    charging =  df.drop(columns=['userInputs'])
    
    # charging = charging.toPandas()
    # creatint a table with information about users
    user_input_0 = df[['userInputs']]
    # user_input = user_input_0.dropna()
    user_list = []
    for i in range(len(user_input_0)):
        df2=pd.DataFrame(user_input_0['userInputs'][i])
        user_list.append(df2)
    users_0=pd.concat(user_list)
    users = users_0.dropna()

    return charging, users

def update_users_datetime(filepath='./data/users.csv'):
    '''
    Changes data type for colums with day, time to datetime.
    '''
    users_to_clean = pd.read_csv(filepath)
    users_to_clean['Modified'] = pd.to_datetime(
        users_to_clean.modifiedAt,
        infer_datetime_format=True)
    users_to_clean['Departure'] = pd.to_datetime(
        users_to_clean.requestedDeparture,
        infer_datetime_format=True)
    users = users_to_clean.drop(columns=[
        'requestedDeparture',
        'modifiedAt',
        'Unnamed: 0'])
    return users


def update_charging_datetime(filepath='./data/charging.csv'):
    charging_to_clean = pd.read_csv(filepath)
    charging_to_clean['ConnectionTime'] = pd.to_datetime(
        charging_to_clean.connectionTime,
        infer_datetime_format=True,utc=True)
    charging_to_clean['DisconnectTime'] = pd.to_datetime(
        charging_to_clean.disconnectTime,
        infer_datetime_format=True,utc=True)
    charging_to_clean['DoneCharging'] = pd.to_datetime(
        charging_to_clean.doneChargingTime,
        infer_datetime_format=True,utc=True)
    # charging_to_clean['ElapsedTime'] = charging_to_clean.DoneCharging - charging_to_clean.ConnectionTime
    charging = charging_to_clean.drop(
        columns=[
            'connectionTime',
            'disconnectTime',
            'doneChargingTime',
            'Unnamed: 0'])
    charging_filter=charging.dropna()      ### drop all row with missing data                          
    return charging_filter


if __name__ == "__main__":
    data_path='/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/'
    file_name='acndata_sessions_office.json'
    charging, users=get_data(file_path=data_path+file_name)
    charging.to_csv('/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data//charging_office.csv')
    users.to_csv('/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/users_office.csv')
    user=update_users_datetime(filepath='/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/users_office.csv')
    user.to_csv('/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/user_office_clean.csv')
    charging=update_charging_datetime(filepath='/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/charging_office.csv')
    charging.to_csv('/media/farzeen/sabrent/sabent/Engergy/EV_charging_demand_prediction/data/charging_office_clean.csv')
    print ('Files users.csv, charging.csv are created.')