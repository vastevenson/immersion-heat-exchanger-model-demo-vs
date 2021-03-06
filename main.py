import matplotlib.pyplot as plt
import math

# define constants
d_o = 9e-3 # IHX outer diam of pipe [=] m
l = 6 # IHX length of pipe submerged [=] m
A_o = math.pi * d_o * l # surface area of the exposed IHX pipes [=] m2
U_o = 1500 # [=] Watts/m2/degree_C - overall Heat Transfer Coef.
# note that IHX inner diameter and thermal conductivity and heat transfer coefficients of the coolant
# and wort liquid are used in the calculation of U_o


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

time_spacing = 10
time_list = list(range(0,1000,time_spacing))

def calc_wort_temp(t):
    # return the temp in the wort (in deg C) at time t (dimensions are seconds)
    return T_ci + (T_ho - T_ci) * math.exp(-(rho_c*Q_c*C_pc)/(rho_h*V_h_m3*C_ph)*((K-1)/K)*t)

wort_temp_list_deg_C = []
for t in time_list:
    wort_temp_list_deg_C.append(calc_wort_temp(t))

def calc_exit_coolant_temp(T_h):
    return T_h - (T_h-T_ci)/K

exit_coolant_temp_list_deg_C = []
for i in wort_temp_list_deg_C:
    exit_coolant_temp_list_deg_C.append(calc_exit_coolant_temp(i))

# create an annotation of the time it takes for the wort temp to reach 25 degrees C (yeast pitching temp)
# find the first value in the wort temp list where the value is < 25
yeast_pitch_temp_deg_C = 25
def get_pitch_time(yeast_pitch_temp_deg_C, wort_temp_list_deg_C, time_spacing):
    t = 0
    for wort_temp in wort_temp_list_deg_C:
        if wort_temp <= yeast_pitch_temp_deg_C:
            return t*time_spacing
        else:
            t += 1
    print('The yeast pitch temperature was never reached.')
    return None

yeast_pitch_time = get_pitch_time(yeast_pitch_temp_deg_C, wort_temp_list_deg_C, time_spacing)


# plotting the points 
plt.plot(time_list, wort_temp_list_deg_C, color='g', label='Wort Temp')

plt.plot(time_list, exit_coolant_temp_list_deg_C, color='b', label='Coolant Exit Temp')

plt.text(400, 50, f"Yeast pitch time (sec): {yeast_pitch_time}", color='m')

# naming the x axis
plt.xlabel('Time, seconds')
# naming the y axis
plt.ylabel('Temperature, degrees C')

# giving a title to my graph
plt.title('Adiabatic Immersion Heat Exchanger Performance')

# add marker at 25 degrees C (when the yeast should be pitched)
plt.axhline(y=25, color='r', linestyle='-')
plt.legend()
# function to show the plot
plt.show()
