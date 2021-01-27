
#############################################################
# Plasma parameters (temperature, density, potential)
# from fitting the characteristics of 
# the initial circuit.
# Input data are probe tension and current.
###########################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats

resistence = 4930   # resistance of the ciruit

# READ DATA FROM TXT
data = pd.read_csv('data.txt', sep = ',')
data = data.apply(pd.to_numeric)

# CALCULATE V PROBE AND I PROBE
Vpr = data['Vtot'] - data['Vr'].sort_values()
Ipr = (data['Vr']/resistence).sort_values()

# ----- PLOT OF I-V CHARACTERISTIC
print('Plotting the I-V Characteristic:')
fig = plt.figure(figsize=(10,10),dpi=300)

plt.scatter(Vpr, Ipr)
plt.grid(True)

plt.xlabel('Probe Voltage [V]')
plt.ylabel('Probe Current [A]')
plt.title('Current - Tension characteristic')
plt.savefig('current_tension_1characteristic.jpg')
plt.show()


#----------------------------------------------------------------------
# CHECK FROM THE PLOT WHAT VALUE OF V IS THE MAX TO HAVE A GOOD LIN FIT
# uncomment to input manualy
"""
VV = float(input('Enter the value [limit to fit Isat]: '))
"""
#fixed value
VV = -5.

# Find the max index to grab every value of V
i=0
while Vpr[i]-VV < 1*math.exp(-16):
    i += 1
   
# VALUES OF LINEAR FIT 
res = stats.linregress(Vpr[0:i], Ipr[0:i])

# --- PLOT CHARACTERISTICS WITH INTERCEPT
print('Plotting the I-V Characteristic with intercept:')
fig = plt.figure(figsize=(10,10),dpi=300)
plt.scatter(Vpr, Ipr)
plt.plot( Vpr, res.slope*Vpr+res.intercept, c = 'red')
plt.grid(True)

plt.xlabel('Probe Voltage [V]')
plt.ylabel('Probe Current [A]')
plt.title('Current - Tension characteristic with Intercept')
plt.text(-60, 0.0010,
         f"R-squared : {res.rvalue**2:.6f}\n"f"Standard error: {res.stderr:.6f}",
         fontsize=10, bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})
plt.savefig('current_tension_2intercept.jpg')
plt.show()


# ---------------------------------------------------------------------
# Subtracting the electron current
Iel=Ipr-(res.slope*Vpr+res.intercept)


# --- PLOT CHARACTERISTICS without electronic current
print('Plotting the I-V Characteristic without saturation electronic current:')
fig = plt.figure(figsize=(10,10),dpi=300)
plt.scatter(Vpr, Iel)
plt.grid(True)

plt.xlabel('Probe Voltage [V]')
plt.ylabel('Probe Current [A]')
plt.title('Current - Tension characteristic without saturation electronic current')
plt.savefig('current_tension_3subtract.jpg')
plt.show()


# --- PLOT CHARACTERISTICS log
print('Plotting the log(I)-V Characteristic in logarithmic scale:')
fig = plt.figure(figsize=(10,10),dpi=300)
plt.scatter(Vpr[i:], Iel[i:])
plt.yscale('log')
plt.ylim(bottom=0.00001)
plt.xlim(left=-70)
plt.grid(True)

plt.xlabel('Probe Voltage [V]')
plt.ylabel('Probe Logarithmic Current [A]')
plt.title('Current - Tension characteristic in log scale')
plt.savefig('current_tension_4log.jpg')
plt.show()

# --------------------------------------------------------------
# fit of the transition zone and the electronic saturation zone

# Uncomment to input manually:
"""
V1 = float(input('Enter the value [low limit to fit transition current]: '))
V2 = float(input('Enter the value [high limit to fit transition current]: '))
V3 = float(input('Enter the value [low limit to fit saturation current]: '))
V4 = float(input('Enter the value [high limit to fit saturation current]: '))
"""

# fixed values
V1=-3
V2=18
V3=20
V4=60

i=j=y=z=0
while Vpr[i] < V1:
    i += 1
while Vpr[j] < V2:
    j += 1
while Vpr[y] < V3:
    y += 1
while Vpr[z] < V4:
    z += 1

res1 = stats.linregress(Vpr[i:j], np.log(Iel[i:j]))
res2 = stats.linregress(Vpr[y:z], np.log(Iel[y:z]))

# --- PLOT CHARACTERISTICS WITH INTERCEPTs
print('Plotting the I-V Characteristic with intercept:')
fig = plt.figure(figsize=(10,10),dpi=300)
plt.scatter(Vpr, np.log(Iel))
plt.plot( Vpr, res1.slope*Vpr+res1.intercept, c = 'red')
plt.plot( Vpr, res2.slope*Vpr+res2.intercept, c = 'red')
plt.grid(True)

plt.xlabel('Probe Voltage [V]')
plt.ylabel('Probe Current [A]')
plt.title('Current - Tension characteristic with Intercept')
plt.text(-40, -3,
         "Transition fit:\n"
         f"R-squared : {res1.rvalue**2:.6f}\n"f"Standard error: {res1.stderr:.6f}\n"
         "Saturation fit:\n"
         f"R-squared : {res1.rvalue**2:.6f}\n"f"Standard error: {res1.stderr:.6f}",
         fontsize=10, bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})
plt.savefig('current_tension_5twofits.jpg')
plt.show()


# -----------------------------------------------------------------
# Useful Values

Aeff = 2.5e-6
me = 9.1e-31
mi = 1836.*me
q = 1.6e-19
Te = 1/(res1.slope)
Vplasma = -((res1.intercept)-(res2.intercept))/((res1.slope)-(res2.slope))
Isat = res.slope*Vpr[0]+res.intercept
ne = abs(Isat)/(0.6*q*(np.sqrt(Te*q/mi))*Aeff)

print("\nElectronic Temperature Te: " + str(Te) + " [eV]")
print("Plasma Potential Vpl: " + str(Vplasma)+ " [V]")
print("Saturation Current Isat: " + str(Isat*1e3) + " [mA]")
print("Electronic Density ne: " + str(ne/1e16) + " [10^16 m-3]")


# electronic sigma (?)
"""
sigma = np.sqrt(np.power((res.stderr/(0.6*q*Aeff)*(np.sqrt(mi/Te))),2)) + 
(np.power(((res1.stderr)*Isat/(0.6*q*Aeff)*(np.sqrt(mi/Te)),2))

print("Sigma: " + str(sigma))
"""