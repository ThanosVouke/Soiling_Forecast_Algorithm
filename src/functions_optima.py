import numpy as np 


def sedimentation(d_p,a_el,rho_aero,rho_air,h_air):
    import numpy as np 
    g = 9.81
    Cu = 1.02
    
    denom = 18*h_air
    
    vs = (np.cos(np.radians(a_el))*g*(d_p**2)*(rho_aero - rho_air)*Cu)/denom
    return vs  
    
    
def brownian(d_p,u_wind,v_air,T_air,h_air,a_br):
    import numpy as np 

    kB = 1.380649e-23 
    T = T_air+273.15
    fract = (3*v_air*np.pi*h_air*d_p)/(kB*T)
    
    vb = a_br*u_wind*(fract**(-0.677))
    return vb 
    
    
def impaction(d_p, rho_aero, u_wind, sigma_or, h_air, a_Im, f_Im, d_Im):
    import numpy as np 

    St1 = rho_aero*d_p**2/(18*h_air)
    St2 = u_wind*sigma_or/d_Im
    St = St1*St2
    
    denom = 1 + np.exp(-f_Im*(St-1))
    
    vim= (a_Im*sigma_or*u_wind)/denom
    
    return vim 


def turbu(d_p, u_wind, a_turb, b_turb, xi_turb,f_turb):
    
    
    a = d_p - xi_turb/u_wind
    b = np.exp(-f_turb*a)
    freb = 1 - 1/(1+b)
    
    vd = a_turb*(1+u_wind*b_turb)*freb
    
    return vd


   
def coverage_rate(V_D, d_p, C_dp, rho):
    
    m = np.pi*(d_p**3)*rho/6
    
    CR =  V_D*(C_dp/m)*(d_p**2)*(np.pi/4)
    
    return CR