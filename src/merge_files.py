import os
import glob
import tqdm 
import pandas as pd
from pysolar import solar
import pvlib 
from pysolar.solar import *


SRC_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(SRC_DIR)

path = os.path.join(PARENT_DIR, "data/Meteorological_Data")

#%% Diavazei ta arxeia 

extension = 'dat'


os.chdir(path)
all_filenames = [i for i in glob.glob('*.dat')]

kean_raw = pd.DataFrame()
df_list= []
for i in tqdm.tqdm(all_filenames):
    df = pd.read_csv(i, skiprows=[0,2,3], index_col=('TIMESTAMP'),usecols=("TIMESTAMP","Tair_Avg", "RH_Avg", "WS_WVc(1)","WS_WVc(2)","Rain_mm_Tot"),parse_dates=(True))
    df_list.append(df)
    
kean_raw = pd.concat(df_list)

#%% Upoligizei tin SZA apo to eniaio arxeio kai to apothikeuei 

Location_lat= float(34.69)

Location_lon= float(33.07)


kean_raw.sort_index(ascending=False)
kean_raw.index = kean_raw.index.tz_localize('UTC')

kean_raw.index = kean_raw.index.tz_localize(None)

kean_raw.rename(columns = {'WS_WVc(1)':'u_wind', 'WS_WVc(2)':'u_dir'}, inplace = True)

kean = kean_raw[kean_raw['u_wind']>0.0]
# kean.to_excel('Kean_merge_data.xlsx')

#%% hourly 

# Ypologismos wriaiwn timwn 

hourly = pd.DataFrame()
hourly['Tair_Avg']=kean .Tair_Avg.resample('h').mean()
hourly['RH_Avg']=kean .RH_Avg.resample('h').mean()
hourly['u_wind']=kean .u_wind.resample('h').mean()
hourly['u_dir']=kean .u_dir.resample('h').mean()
hourly['Rain_mm']=kean .Rain_mm_Tot.resample('h').sum()


hourly.index = hourly.index.tz_localize('UTC')

date = hourly.index.to_pydatetime() #transformed to the right form

SZAs = []
el = [] 
az = []
for date_v in tqdm.tqdm(date):
    
    SZAs.append(round(90 - solar.get_altitude(Location_lat,Location_lon,date_v), 5))   #calculate the Solar Zenith Angle
    el.append(solar.get_altitude(Location_lat,Location_lon,date_v))
    az.append(solar.get_azimuth(Location_lat, Location_lon, date_v))
    
hourly['SZA'] = SZAs
hourly['el']= el 
hourly['az'] = az

hourly.index = hourly.index.tz_localize(None)

