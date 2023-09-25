
from datetime import datetime, timedelta
start = datetime.now()

from constants  import *
from model_parameters import *
from functions_optima import *
import os
from pysolar import solar
import pandas as pd
import tqdm 
import xarray as xr
import openpyxl
from ads import ads
from merge_files import hourly#, kean
import numpy as np
pwd = os.getcwd()
from windrose import WindroseAxes
import matplotlib.cm as cm
from IPython.display import Image
import shutil

SRC_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(SRC_DIR)


# %%------------------------------------------------------------------------1st Stage------------------------------------------------------ 

ads= ads.astype(np.float64)
hourly= hourly.astype(np.float64)
hourly = hourly[hourly.index >'2019-06-01']      

df = pd.concat([hourly, ads], axis=1)


df['thetta_mirror'] = 'NaN'

df['thetta_mirror'] = np.where( df['az'] > Location_bear_angle, Location_bear_angle-90, Location_bear_angle+90 )

df['elev_angle'] = np.where(df['el']>0,df['SZA'], np.nan)



df= df.astype(np.float64)

df['vs'] = sedimentation(Particle_size_d_p,df['elev_angle'],rho_aero,rho_air,h_air)   #gia ta  2.5 - 10 
df['vs_2p5']= sedimentation(Particle_size_d_p2p5,df['elev_angle'],rho_aero,rho_air,h_air)   # gia ta 0-2.5 
df['vs_029'] = sedimentation(Particle_size_d_p029,df['elev_angle'],rho_aero,rho_air,h_air)    # gia to 2o montelo 0.03 - 0.55
df['vs_07']  = sedimentation(Particle_size_d_p07, df['elev_angle'], rho_aero, rho_air, h_air)   #  0.55- 0.9
df['vs_10'] = sedimentation(Particle_size_d_p10, df['elev_angle'], rho_aero, rho_air, h_air)   #  0.9 - 20



df['vb'] =  brownian(Particle_size_d_p,df['u_wind'],v_air,df['Tair_Avg'],h_air,Model_param_a_br)
df['vb_2p5'] =  brownian(Particle_size_d_p2p5,df['u_wind'],v_air,df['Tair_Avg'],h_air,Model_param_a_br)
df['vb_029'] =   brownian(Particle_size_d_p029,df['u_wind'],v_air,df['Tair_Avg'],h_air,Model_param_a_br)
df['vb_07']  =  brownian(Particle_size_d_p07,df['u_wind'],v_air,df['Tair_Avg'],h_air,Model_param_a_br)
df['vb_10']  =  brownian(Particle_size_d_p10,df['u_wind'],v_air,df['Tair_Avg'],h_air,Model_param_a_br)


df['dtheta'] = (df['u_dir'] - df['thetta_mirror'])%360
df['p']= np.cos(np.radians(df['dtheta']))* np.sin(np.radians(df['elev_angle']))


df['sigma_or']= np.where( df['p']>0, df['p'] , 0 )


        
df['v_Im'] = impaction(Particle_size_d_p,rho_aero,df['u_wind'],df['sigma_or'],h_air,Model_param_a_Im,Model_param_f_Im,Model_param_d_Im)
df['v_Im_2p5'] =  impaction(Particle_size_d_p2p5,rho_aero,df['u_wind'],df['sigma_or'],h_air,Model_param_a_Im,Model_param_f_Im,Model_param_d_Im)
df['v_Im_029'] =   impaction(Particle_size_d_p029,rho_aero,df['u_wind'],df['sigma_or'],h_air,Model_param_a_Im,Model_param_f_Im,Model_param_d_Im) 
df['v_Im_07']  =  impaction(Particle_size_d_p07,rho_aero,df['u_wind'],df['sigma_or'],h_air,Model_param_a_Im,Model_param_f_Im,Model_param_d_Im)
df['v_Im_10']  =  impaction(Particle_size_d_p10,rho_aero,df['u_wind'],df['sigma_or'],h_air,Model_param_a_Im,Model_param_f_Im,Model_param_d_Im)


df= df.astype(np.float64)

df['V_D'] = np.where(df['u_wind']<6.8, df['vs'].fillna(0) + df['vb'].fillna(0) + df['v_Im'].fillna(0), 
                     turbu(Particle_size_d_p, df['u_wind'], Model_param_a_turb, Model_param_b_turb, Model_param_xi_turb, Model_param_f_turb))

df['V_D2p5'] = np.where(df['u_wind']<6.8, df['vs_2p5'].fillna(0)+ df['vb_2p5'].fillna(0)+df['v_Im_2p5'].fillna(0), 
                     turbu(Particle_size_d_p2p5, df['u_wind'], Model_param_a_turb, Model_param_b_turb, Model_param_xi_turb, Model_param_f_turb))

df['V_D_029'] = np.where(df['u_wind']<6.8, df['vs_029'].fillna(0)+df['vb_029'].fillna(0) +df['v_Im_029'].fillna(0), 
                     turbu(Particle_size_d_p029, df['u_wind'], Model_param_a_turb, Model_param_b_turb, Model_param_xi_turb, Model_param_f_turb))

df['V_D_07'] = np.where(df['u_wind']<6.8,df['vs_07'].fillna(0)+df['vb_07'].fillna(0)+df['v_Im_07'].fillna(0), 
                     turbu(Particle_size_d_p07, df['u_wind'], Model_param_a_turb, Model_param_b_turb, Model_param_xi_turb, Model_param_f_turb))

df['V_D_10'] = np.where(df['u_wind']<6.8,df['vs_10'].fillna(0)  +df['vb_10'].fillna(0)+ df['v_Im_10'].fillna(0), 
                    turbu(Particle_size_d_p10, df['u_wind'], Model_param_a_turb, Model_param_b_turb, Model_param_xi_turb, Model_param_f_turb))


df['V_D_2p5_10'] = df['V_D']+  df['V_D2p5']  # einai gia 0-2.5 + 2.5-10, dld to sunoliko gia to montelo 1
df['V_D_model2'] = df['V_D_029'] +  df['V_D_07']  + df['V_D_10']  # auto einai gia to sunoliko gia to montelo 2
 
   
df['rhr'] = np.round(df['RH_Avg'],-1)
    
    
    
rHfactor_10 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ,
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [ 0.7, 0.75, 0.8, 0.9, 1, 1, 1, 1, 1, 1, 1],
                [ 0.35, 0.4, 0.5, 0.7, 0.8, 0.9, 1, 1, 1, 1, 1],
                [0, 0.1, 0.15, 0.3, 0.5, 0.7, 0.8, 1, 1, 1, 1],            
                [0, 0, 0, 0, 0.08, 0.2, 0.5, 0.85, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0.15, 0.5, 0.85, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0.1, 0.4, 0.9, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0.08, 0.6, 0.85],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.6]]  

rHfactor_10 = np.array(rHfactor_10)

df = df[df['rhr'].notna()]

df['rebound'] = 'NaN'

for i in tqdm.tqdm(range(len(df))):
    
    if df['u_wind'][i]<3 :
        df['rebound'][i] = 1
    else:
        df['rebound'][i] = rHfactor_10[3,int(np.floor(df['rhr'][i]/10))]
        
    
    
df['cr_pm'] = coverage_rate(df['V_D'],Particle_size_d_p,df['pm'],rho)
df['cr_2p5'] = coverage_rate(df['V_D2p5'],Particle_size_d_p2p5,df['pm2p5'],rho)
df['CR1'] = df['cr_pm'] + df['cr_2p5']



df['cr_029'] =  coverage_rate(df['V_D_029'] ,Particle_size_d_p029,df['Da1'],rho)
df['cr_07']  =  coverage_rate(df['V_D_07'],Particle_size_d_p07,df['Da2'],rho)
df['cr_10']  =  coverage_rate(df['V_D_10'],Particle_size_d_p10,df['Da3'],rho)*df['rebound']
df['CR2'] = df['cr_029'] + df['cr_07'] + df['cr_10']


#%%----------------------------------------------------------------2nd Stage----------------------------------------------------------


path = os.path.join(PARENT_DIR, "data")

os.chdir(path)


ref = pd.read_excel('Refl. Avg measurements.xlsx',header=0,index_col='Date',parse_dates=True)



os.chdir(pwd)



dfin =  pd.concat([df,ref], axis=1) 
# dialy 

dfinf = pd.DataFrame()

dfinf['CR1']= dfin['CR1']
dfinf['cr_2p5'] = dfin['cr_2p5']
dfinf['cr_pm'] = dfin['cr_pm']
dfinf['Rain_mm'] = dfin['Rain_mm']
dfinf['CR2']=dfin['CR2']
dfinf['cr_029'] = dfin['cr_029']
dfinf['cr_07'] = dfin['cr_07']
dfinf['cr_10'] = dfin['cr_10']
dfinf['Da1'] = dfin['Da1']         
dfinf['Da2']= dfin['Da2']
dfinf['Da3']= dfin['Da3']

dfinf = dfinf.astype(np.float64)
dfinf = dfinf.resample('24h', base=9).sum()

dff = pd.DataFrame()

dff['V_D_2p5_10'] = dfin['V_D_2p5_10']
dff['V_D_model2'] = dfin['V_D_model2'] 
dff['V_D_10'] = dfin['V_D_10'] 
dff['V_D_2p5_10'] = dfin['V_D_2p5_10'] 
dff['pm'] = dfin['pm'] 
dff['pm2p5'] = dfin['pm2p5'] 
dff['duaod550'] = dfin['duaod550']

dff = dff.astype(np.float64)
dff = dff.resample('24h', base=9).mean()


ref= ref.astype(np.float64)
refD = ref.resample('24h', base=9).mean()

file1 = pd.concat([dff,dfinf], axis=1)


dffind = pd.concat([file1,ref], axis=1)  


# Soiling Rate gia to 1o 
df['SR1'] = df['CR1']*Model_param_prop_factor_model_1

# Soiling Rate gia to 2o 
df['SR2'] = df['CR2'].dropna()*Model_param_prop_factor_model_2
df= df.astype(np.float64)

# compute Soiling rate for model 1
dffind['SR1'] = dffind['CR1']*Model_param_prop_factor_model_1

#compute percentage of subCR to the total soiling rate
dffind['perce_cr_mp'] = (dffind['cr_pm']*Model_param_prop_factor_model_1/dffind['SR1'])*100
dffind['perce_cr_2p5'] = (dffind['cr_2p5']*Model_param_prop_factor_model_1/dffind['SR1'])*100


# compute soiling rate for Model 2
dffind['SR2'] = dffind['CR2']*Model_param_prop_factor_model_2
    
#compute percentage of subCR to the total soiling rate
dffind['perce_cr_029'] = (dffind['cr_029']*Model_param_prop_factor_model_2/dffind['SR2'])*100
dffind['perce_cr_07'] = (dffind['cr_07']*Model_param_prop_factor_model_2/dffind['SR2'])*100
dffind['perce_cr_100'] = (dffind['cr_10']*Model_param_prop_factor_model_2/dffind['SR2'])*100


#%% change of soiling rate due to rain 


#SR1 clear rain 
df['SR1'] = np.where( (df['Rain_mm']>0) & (df['Rain_mm']<= 1) & (df['duaod550']<= 0.3),  -0.02, df['SR1'] )  #Rain 0mm - 1mm 
df['SR1'] = np.where( (df['Rain_mm']>1) & (df['Rain_mm']<= 2)& (df['duaod550']<= 0.3), - 0.01, df['SR1'] )
df['SR1'] = np.where( (df['Rain_mm']>2) & (df['Rain_mm']<= 3)& (df['duaod550']<= 0.3), - 0.0075, df['SR1'] )
df['SR1'] = np.where( (df['Rain_mm']>3) & (df['Rain_mm']<= 4)& (df['duaod550']<= 0.3), - 0.004, df['SR1'] )
df['SR1'] = np.where( (df['Rain_mm']>4) & (df['duaod550']<= 0.3), - 0.0015, df['SR1'] )

#SR1 red rain 

df['SR1'] = np.where( (df['Rain_mm']>0) & (df['aod550']> 0.3), 0.02, df['SR1'] )

#SR2
df['SR2'] = np.where( (df['Rain_mm']>0) & (df['Rain_mm']<= 1) & (df['duaod550']<= 0.3), - 0.02, df['SR2'] )  #Rain 0mm - 1mm 
df['SR2'] = np.where( (df['Rain_mm']>1) & (df['Rain_mm']<= 2) & (df['duaod550']<= 0.3), - 0.01, df['SR2'] )
df['SR2'] = np.where( (df['Rain_mm']>2) & (df['Rain_mm']<= 3) & (df['duaod550']<= 0.3), - 0.0075, df['SR2'] )
df['SR2'] = np.where( (df['Rain_mm']>3) & (df['Rain_mm']<= 4) & (df['duaod550']<= 0.3), - 0.004, df['SR2'] )
df['SR2'] = np.where( (df['Rain_mm']>4) & (df['duaod550']<= 0.3) ,  - 0.0015, df['SR2'] )

#SR2 red rain 

df['SR2'] = np.where( (df['Rain_mm']>0) & (df['aod550']> 0.3), 0.02, df['SR2'] )



#Daily 
#SR1 clear rain 
dffind['SR1'] = np.where( (dffind['Rain_mm']>0) & (dffind['Rain_mm']<= 1) & (dffind['duaod550']<= 0.3),  -0.02, dffind['SR1'] )  #Rain 0mm - 1mm 
dffind['SR1'] = np.where( (dffind['Rain_mm']>1) & (dffind['Rain_mm']<= 2)& (dffind['duaod550']<= 0.3), - 0.01, dffind['SR1'] )
dffind['SR1'] = np.where( (dffind['Rain_mm']>2) & (dffind['Rain_mm']<= 3)& (dffind['duaod550']<= 0.3), - 0.0075, dffind['SR1'] )
dffind['SR1'] = np.where( (dffind['Rain_mm']>3) & (dffind['Rain_mm']<= 4)& (dffind['duaod550']<= 0.3), - 0.004, dffind['SR1'] )
dffind['SR1'] = np.where( (dffind['Rain_mm']>4) & (dffind['duaod550']<= 0.3), - 0.0015, dffind['SR1'] )

#SR1 red rain 

dffind['SR1'] = np.where( (dffind['Rain_mm']>0) & (dffind['duaod550']> 0.3), 0.055, dffind['SR1'] )


#SR2
dffind['SR2'] = np.where( (dffind['Rain_mm']>0) & (dffind['Rain_mm']<= 1) & (dffind['duaod550']<= 0.3), - 0.02, dffind['SR2'] )  #Rain 0mm - 1mm 
dffind['SR2'] = np.where( (dffind['Rain_mm']>1) & (dffind['Rain_mm']<= 2) & (dffind['duaod550']<= 0.3), - 0.01, dffind['SR2'] )
dffind['SR2'] = np.where( (dffind['Rain_mm']>2) & (dffind['Rain_mm']<= 3) & (dffind['duaod550']<= 0.3), - 0.0075, dffind['SR2'] )
dffind['SR2'] = np.where( (dffind['Rain_mm']>3) & (dffind['Rain_mm']<= 4) & (dffind['duaod550']<= 0.3), - 0.004, dffind['SR2'] )
dffind['SR2'] = np.where( (dffind['Rain_mm']>4) & (dffind['duaod550']<= 0.3) ,  - 0.0015, dffind['SR2'] )


#SR1 red rain 

dffind['SR2'] = np.where( (dffind['Rain_mm']>0) & (dffind['duaod550']> 0.3), 0.055, dffind['SR2'] )

#%% convert soiling rate to reflectivity 

# r : reflectivity accumulative model 1
dffind['r'] = 'NaN'
dffind['r'][0] = Model_param_r_clean

#reflectivity daily prediction model 1
dffind['rdp'] = 'NaN'
dffind['rdp'][0] = Model_param_r_clean

# rSRmodel2 : reflectivity accumulative model 2
dffind['rSRmodel2']= 'NaN'
dffind['rSRmodel2'][0] = Model_param_r_clean

# reflectivity daily prediction model 2
dffind['rSRmodel2_dp']= 'NaN'
dffind['rSRmodel2_dp'][0] = Model_param_r_clean


dffind['rcum']='NaN'    #rcum : accumulative sum of reflectivity calculated from soiling of model 1 initialize the refl at 0.96
dffind['rcumm2']='NaN'  # the same reflectivity prediction as above, based on soiling estimation from model 2



date = ref.index[26] # Date = 2019-06-02

dffind['N'] = dffind.reset_index().index

location = dffind.loc[dffind.index == date, ['N']].values[0][0]

# initialize the refl at 0.96 from soiling of model 1
dffind.loc[dffind.index == date, ['rcum']] = dffind['AVG'][location]
# initialize the refl at 0.96 from soiling of model 2
dffind.loc[dffind.index == date, ['rcumm2']] = dffind['AVG'][location]



for i in tqdm.tqdm(range(location+1, location+5)):
                 
    dffind['rcum'][i] = dffind['rcum'][i-1] - Model_param_r_clean*dffind['SR1'][i-1]
    dffind['rcumm2'][i] =  dffind['rcumm2'][i-1] -  Model_param_r_clean*dffind['SR2'][i-1] 
    
    

#%% ------------------------------------------------------------------------3rd Stage------------------------------------------------------- 

df['rcum']='NaN'  
df['rcum'][0] = dffind['AVG'][location]   #rcum : accumulative sum of reflectivity calculated from soiling of model 1 initialize the refl at 0.96
df['rcumm2']='NaN'
df['rcumm2'][0] = dffind['AVG'][location]  # the same reflectivity prediction as above, based on soiling estimation from model 2

SR2 = pd.DataFrame()
SR2['SR'] = df['SR2'].dropna()
SR2['refl'] = np.nan
SR2['refl'][0]= dffind['AVG'][location]
SR2= SR2.astype(np.float64)


dffind = dffind.loc[ date :  date+ timedelta(days=4)]

df= df.astype(np.float64)
dffind= dffind.astype(np.float64)

from matplotlib import ticker
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, dpi=600, figsize=(16,12),sharex=True)


ax[0].yaxis.set_tick_params(labelsize=20)

ax[0].scatter(dffind.index,dffind['AVG'],s=250, color='black', label='Measurments')

ax[0].plot(dffind['rcum'].dropna(), '--o', linewidth=3, markersize=15,label='Model 1')



ax[0].set_yticks(np.arange(0.86,0.99,0.01))
ax[0].legend(fontsize=20)
ax[0].grid(linewidth=2)

ax[0].set_ylabel('Refl(%) accumulative prediction - Model 1', fontsize = 18)


ax[1].yaxis.set_tick_params(labelsize=20)

ax[1].scatter(dffind.index,dffind['AVG'],s=250, color='black', label='Measurments')
ax[1].plot(dffind['rcumm2'].dropna(), '--o',linewidth=3, markersize=15, label='Model 2')
ax[1].legend(fontsize=20)
ax[1].set_yticks(np.arange(0.86,0.99,0.01))
ax[1].set_ylabel('Refl(%) accumulative prediction - Model 2', fontsize=18)
ax[1].grid(linewidth=2)


fig.subplots_adjust(top=0.96)
fig.suptitle('Reflectivity June 2019 - 4 days prediction vs reflectometer measurements', fontsize=20)
plt.xticks(fontsize=20)
plt.tight_layout()
plt.savefig('SR_'+ str(date.day) + '_' + date.strftime('%B')+ '_' +date.strftime('%Y')+'.jpg')
plt.show() 
path = os.path.join(PARENT_DIR, "output/Plots")
shutil.move('SR_'+ str(date.day) + '_' + date.strftime('%B')+ '_' +date.strftime('%Y')+'.jpg', path)


#%%  Hourly reflectivity 




for i in tqdm.tqdm(range(1,len(SR2))):
    SR2['refl'][i] = SR2['refl'][i-1] - Model_param_r_clean*SR2['SR'][i-1]
    
    

for i in tqdm.tqdm(range(1,len(df))):
    df['rcum'][i] = df['rcum'][i-1] - Model_param_r_clean*df['SR1'][i-1]
    
df = df.loc[ date :  date+ timedelta(days=4)]
df =pd.concat([df, SR2], axis=1)


path = os.path.join(PARENT_DIR, "output")
dffind.to_excel(f"{path}/Daily_SR_{date.year}_{date.month}_{date.day}.xlsx", index_label='Time', header= True)
df.to_excel(f"{path}/Hourly_{date.year}_{date.month}_{date.day}.xlsx", index_label='Time', header= True)

df['sedi_1'] = df['vs'] + df['vs_2p5'] 
df['brow_1'] = df['vb'] + df['vb_2p5']
df['impa_1'] = df['v_Im'] + df['v_Im_2p5']

df['sedi_2'] = df['vs_029'] + df['vs_07'] +  df['vs_10']
df['brow_2'] = df['vb_029'] + df['vb_07'] +  df['vb_10']
df['impa_2'] = df['v_Im_029'] + df['v_Im_07'] +  df['v_Im_10']


d_1 = {'pm2p5':{'Title': r' PM2.5 (kg/$m^3$)', 'color':'Blue'}, 
       'pm':{'Title':r' PM10-2.5 (kg/$m^3$)', 'color':'red'},
       'V_D_2p5_10':{'Title':'Deposition velocity (m/s)', 'color':'green'}, 
       'SR1':{'Title':'Soiling rate (%)', 'color':'red'}, 
       'rcum':{'Title':'Forecast reflectivity (%)', 'color':'black'}}



d_2 = {'sedi_1':{'Title':'Velocity from Sedimentation (m/s)', 'color':'Blue'},
       'brow_1':{'Title':'Velocity from Brownian (m/s)', 'color':'red'},
       'impa_1':{'Title':'Velocity from Impaction (m/s)', 'color':'green'},
       "u_wind":{"Title": 'Wind speed (m/s)' , 'color':'red'}, 
       'u_dir':{'Title':'Wind direction', 'color':'Black'}}


d_3 = {'duaod550':{'Title':'Dust aerosol optical depth 550nm', 'color':'Blue'}, 
       'aod550':{'Title':'Total aerosol optical depth 500nm', 'color':'red'},
       'Tair_Avg' :{'Title':'Air temperature ($^\circ$C)', 'color':'green'},
       'RH_Avg':{'Title':'Relative humidity (%)', 'color':'red'},
       'Rain_mm':{'Title':'Hourly precipitation (mm)', 'color':'blue'}}


d_4 = {'Da1':{'Title':'Dust aerosol (0.03-0.55μm) mixing ratio (kg/kg)', 'color':'blue'},
       'Da2':{'Title':'Dust aerosol (0.55-0.9μm) mixing ratio (kg/kg)', 'color':'red'},
       'Da3':{'Title':'Dust aerosol (0.9-20μm) mixing ratio (kg/kg)', 'color':'green'}, 
       'SR2':{'Title':'Soiling rate (%)', 'color':'red'},
       'refl':{'Title':'Forecast reflectivity (%)', 'color':'black'}}



d_5 = {'sedi_2':{'Title':'Velocity from Sedimentation (m/s)', 'color':'Blue'},
       'brow_2':{'Title':'Velocity from Brownian (m/s)', 'color':'red'},
       'impa_2':{'Title':'Velocity from Impaction (m/s)', 'color':'green'},
       "u_wind":{"Title": 'Wind speed (m/s)' , 'color':'red'}, 
       'u_dir':{'Title':'Wind direction', 'color':'Black'}}


li = [d_1, d_2, d_3, d_4, d_5]

path = os.path.join(PARENT_DIR, "output/Plots")

for l,j in enumerate(li):
    fig, ax = plt.subplots(5,  figsize=(16,12),sharex=True)
    
    for i, k in enumerate(j.keys()):
        if k== 'Da1' or k=='Da2' or k=='Da3' or k=='SR2' or k=='refl':
            ax[i].yaxis.set_tick_params(labelsize=20)
            ax[i].plot(df[k].dropna(), color=j[k]['color'])
            ax[i].grid()
            ax[i].set_title(j[k]['Title'], fontsize = 18, rotation = 0)
        elif k =='Rain_mm':
            ax[i].yaxis.set_tick_params(labelsize=20)
            ax[i].bar(df.index, df[k])
            ax[i].set_xlim(df.index.min(),df.index.max())
            ax[i].grid()
            ax[i].set_title(j[k]['Title'], fontsize = 18, rotation = 0)
        else:
            ax[i].yaxis.set_tick_params(labelsize=20)
            ax[i].plot(df[k], color=j[k]['color'])
            ax[i].grid()
            ax[i].set_title(j[k]['Title'], fontsize = 18, rotation = 0)
    
    fig.subplots_adjust(top=0.98)
    # fig.suptitle('Model 1', fontsize=20)
    plt.xticks(fontsize=20)
    plt.tight_layout()
    if l<2:
        plt.savefig('Model 1_'+str(l)+'.jpg')
        plt.show()
        plt.close()
        shutil.move('Model 1_'+str(l)+'.jpg', path)
    elif l==2 :
        plt.savefig('Aod.jpg')
        plt.show()
        plt.close()
        shutil.move('Aod.jpg', path)
    else :
        plt.savefig('Model 2_'+str(l)+'.jpg')
        plt.show()
        plt.close()
        shutil.move('Model 2_'+str(l)+'.jpg', path)




# windrose 



split = np.array_split(df,4) # split the dataframe in 4 parts, for each forecast day 

for i in range(0,4):
    ax = WindroseAxes.from_ax()
    
    ax.bar(split[i]['u_dir'].dropna(), split[i]['u_wind'].dropna(),edgecolor='k',bins=4, normed=True,opening=0.8,cmap=cm.jet)    
    plt.savefig('Windrose_'+str(split[i].index.min())[:-9]+ ' - ' +str(split[i].index.max())[:-9]+'.png')
    plt.close()
    shutil.move('Windrose_'+str(split[i].index.min())[:-9]+ ' - ' +str(split[i].index.max())[:-9]+'.png', path)
    
    


print(datetime.now() - start)
