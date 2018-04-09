import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import seaborn as sns
from scipy import stats

weather_map = {'Mostly Clear': 4, 'Extreme Rainstorm': 35, 'Light Rain': 30, 'Snow': 37, 'Haze': 21, 'Fog': 14, 'Light Snow': 36, 'Thundershower': 22, 'Needle Ice': 27, 'Sunny': 1, 'Thunderstorm': 24, 'Rain': 31, 'Freezing Fog': 15, 'Light Snow Showers': 13, 'Dust': 17, 'Snow Showers': 12, 'Freezing Rain': 40, 'Heavy Snow': 38, 'Thundershower with Hail': 25, 'Clear': 2, 'Overcast': 7, 'Cloudy': 5, 'Lightning': 23, 'Sandstorm': 16, 'Sand': 19, 'Partly Cloudy': 6, 'Dust Storm': 18, 'Scattered Showers': 9, 'Mostly Sunny': 3, 'Blizzard': 39, 'Heavy Rainstorm': 34, 'Heavy Sandstorm': 20, 'Icy': 28, 'Hail': 26, 'Sleet': 29, 'Heavy Rain': 32, 'Rainstorm': 33, 'Showers': 8, 'Light Showers': 10, 'Heavy Showers': 11}
station_map = {
 'aotizhongxin': 32,
 'badaling': 22,
 'beibuxinqu': 8,
 'daxing': 12,
 'dingling': 31,
 'donggaocun': 14,
 'dongsi': 23,
 'dongsihuan': 6,
 'fangshan': 15,
 'fengtaihuayuan': 3,
 'guanyuan': 24,
 'gucheng': 11,
 'huairou': 1,
 'liulihe': 7,
 'mentougou': 9,
 'miyun': 30,
 'miyunshuiku': 27,
 'nansanhuan': 21,
 'nongzhanguan': 2,
 'pingchang': 35,
 'pinggu': 29,
 'qianmen': 10,
 'shunyi': 28,
 'tiantan': 13,
 'tongzhou': 4,
 'wanliu': 19,
 'wanshouxigong': 18,
 'xizhimenbei': 25,
 'yanqin': 33,
 'yizhuang': 20,
 'yongdingmennei': 16,
 'yongledian': 26,
 'yufa': 5,
 'yungang': 34,
 'zhiwuyuan': 17
 }

def find_weather_code(x):
    x = x.split('/')[0]
    if x in weather_map.keys():
        return weather_map[x]
    else:
        for key in weather_map.keys():
            if key in x:
                return weather_map[key]
        return -1

def find_station_code(x):
    if x in station_map.keys():
        return station_map[x]

def count_null(data):
    na_count = data.isnull().sum().sort_values(ascending=False)
    na_ratio = na_count / len(data)
    na_data = pd.concat([na_count,na_ratio],axis=1,keys=['count','ration'])
    return na_data

def predict_null(data_merge,feature_missing):
    feature_drop = ["PM2.5","PM10","NO2","CO","O3","SO2"]
    y_train = data_merge[feature_missing][data_merge[feature_missing].notnull()].values
    x_train = data_merge[data_merge[feature_missing].notnull()].drop(feature_drop,axis=1).fillna(method='ffill')
    x_test = data_merge[data_merge[feature_missing].isnull()].drop(feature_drop,axis=1).fillna(method='ffill').values

    from sklearn.ensemble import RandomForestRegressor
    rfr = RandomForestRegressor().fit(x_train,y_train)
    data_merge[feature_missing][data_merge[feature_missing].isnull()] = rfr.predict(x_test)
    return data_merge




def merge_data(data_aq,data_meo):

    # merge data through keys on ['station_name','utc_time']
    data_aq['station_name'] = data_aq['stationId'].map(lambda x: x[:-3])
    data_meo['station_name'] = data_meo['station_id'].map(lambda x: x[:-4])
    data_merge = pd.merge(data_aq,data_meo,on=['station_name','utc_time'],how='inner')

    # build training data using features chosen 
    feature_chosen = ['station_name','temperature',
                    'pressure','humidity','wind_direction','wind_speed','weather','PM2.5','PM10','NO2','CO','O3','SO2']
    data_merge = pd.DataFrame(data_merge,columns=feature_chosen)

    # map weather label into number
    data_merge['weather'] = data_merge['weather'].apply(find_weather_code)
    data_merge['station_name'] = data_merge['station_name'].apply(find_station_code)

    return data_merge

def process(data_aq,data_meo):
    pass

