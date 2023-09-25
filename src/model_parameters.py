#%%laminar model
Model_param_a_br = 0.164  # factor for Brownian motion
Model_param_a_Im = 0.0017  # factor for Impaction
Model_param_d_Im = 6.56e-06 # factor for Impaction
Model_param_f_Im = 19.3    # factor for impaction, Stokes


#%% turbulent regime model

Model_param_a_turb = 0.057
Model_param_b_turb = 0.19
Model_param_f_turb = 2.06e05
Model_param_xi_turb = 9.4e-05

# define turbulent threshold
Model_param_turbul_threshold = 6.8

# proportionality factors
Model_param_prop_factor_model_1 = 4.1e04    
Model_param_prop_factor_model_2 = 9.5e04   

# reflectivity of clean CSP mirrors
Model_param_r_clean= 0.95         #reflectivity of clean mirror
