import matplotlib.pyplot as plt
import math

# define constants
d_o = 9e-3 # IHX outer diam of pipe [=] m
l = 6 # IHX length of pipe submerged [=] m
A_o = math.pi * d_o * l # surface area of the exposed IHX pipes [=] m2
U_o = 1500 # [=] Watts/m2/degree_C - overall Heat Transfer Coef.

rho_c = 1000 # density of coolant, kg/m3
Q_c_lpm = 4 # vol flow rate of coolant, L/min
Q_c = Q_c_lpm / 1000 / 60 # vol flow rate coolant, m3/s
C_pc = 4184 # specific heat capacity coolant [=] J/kg/deg_K

# note K is a dimensionless, as is the argument to the exp()!
K = math.exp((U_o*A_o)/(rho_c*Q_c*C_pc))

T_ci = 15 # inlet coolant temp, deg_C
T_ho = 100 # initial wort temp, deg_C

# wort parameters
rho_h = 1000 # kg/m3, density of the wort - assume to be that of water
V_h_gal = 3 # volume of the wort's liquid, in gal
V_h_m3 = V_h_gal / 264 # vol of wort liquid, in m3
C_ph = 4184 # specific heat capacity of wort liquid, J/kg/deg_C

time_list = list(range(0,1000,10))

def calc_wort_temp(t):
    # return the temp in the wort (in deg C) at time t
    return T_ci + (T_ho - T_ci) * math.exp(-(rho_c*Q_c*C_pc)/(rho_h*V_h_m3*C_ph)*((K-1)/K)*t)

wort_temp_list_deg_C = []
for t in time_list:
    wort_temp_list_deg_C.append(calc_wort_temp(t))

# plotting the points 
plt.plot(time_list, wort_temp_list_deg_C)

# naming the x axis
plt.xlabel('Time, minutes')
# naming the y axis
plt.ylabel('Temperature of the wort, degrees C')

# giving a title to my graph
plt.title('Immersion Heat Exchanger Performance')

# function to show the plot
plt.show()

print()