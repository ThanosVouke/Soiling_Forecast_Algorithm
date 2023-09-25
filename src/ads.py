import xarray as xr 
import os 
import glob 
import tqdm 
import pandas as pd
pwd = os.getcwd()

SRC_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(SRC_DIR)

#%% first model 


path = os.path.join(PARENT_DIR, "data/PM/sfc")


os.chdir(path)
all_filenames = [i for i in glob.glob('*.nc')]



df_list = [] 

for i in  tqdm.tqdm(all_filenames):
    nc = xr.open_dataset(i)
    df = nc.to_dataframe()
    df_list.append(df)

ads1 =  pd.concat(df_list)

ads1 = ads1.reset_index('latitude')
ads1 = ads1.reset_index('longitude')

ads1 = ads1.reset_index('time')
ads1 = ads1.sort_values(by=['time'])
ads1 = ads1.set_index(ads1.time, drop=True)


del  ads1['latitude'] ,ads1['longitude']
del ads1['time']



ads1['pm']=ads1['pm10'] - ads1['pm2p5']



ads1 = ads1[~ads1.index.duplicated(keep='first')]   # diwnxei ta dyplicates, einai SOS entoli 



#%% second model 

path = os.path.join(PARENT_DIR, "data/PM/ml")

os.chdir(path)
all_filenames = [i for i in glob.glob('*.nc')]


df_list = [] 


for i in  tqdm.tqdm(all_filenames):
    nc = xr.open_dataset(i)
    df = nc.to_dataframe()
    df_list.append(df)

ads2 =  pd.concat(df_list)  # ta vazei ola se ena arxeio 


ads2 = ads2.reset_index('latitude')
ads2 = ads2.reset_index('longitude')

ads2 = ads2.reset_index('time')
ads2 = ads2.sort_values(by=['time'])
ads2 = ads2.set_index(ads2.time, drop=True)


del  ads2['latitude'] ,ads2['longitude']
del ads2['time']

ads2.rename(columns = {'aermr04':'Da1', 'aermr05':'Da2', 'aermr06':'Da3'}, inplace = True)


ads2 = ads2[~ads2.index.duplicated(keep='first')]


ads = pd.concat([ads1, ads2], axis=1) # sychronized data from copernicus for both models 


        
ads.index = ads.index.tz_localize(None)


path = pwd
os.chdir(path)
