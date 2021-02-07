######################################################################
# The resistance of 5kO was too much for the amplificator range.
# the new resistance is of 1kO.
# Now the data are the real one from the Langmuir probe.
# Input data are probe tension and current.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
from scipy import stats
import scipy.odr as odr


# READ DATA FROM TXT
data = pd.read_csv('data.txt', sep = ',')
data = data.apply(pd.to_numeric)

Ampl = 7.41  # amplification factor
RES = 1000  # resistance

# CALCULATE V PROBE AND I PROBE
Vpr = (data['Vtot'] - data['Vr'])#*Ampl
Ipr = (data['Vr']/RES)

# Add and subtract the parasitic capacity to negative and positive signal slopes
i = 0
for i in range(len(Vpr)-1):
    if Vpr[i] < Vpr[i+1]:
        Ipr[i] = Ipr[i] - 1.5e-5
    else:
        Ipr[i] = Ipr[i] + 1.5e-5

Vpr = Vpr-RES*Ipr

# Starting fit parameters
Isat=-0.0002
alfa=1.  # correction parameter
Vfl=5
Temp=4.

cost = 4.256e14
Vfin = 2 # starting fit value

# Sort data in order to evaluate them in ranges
Data = list(sorted(zip(Vpr,Ipr)))
lenVpr = len(Vpr)
Vpr = []
Ipr = []

for i in range(lenVpr):
    Vpr.append(Data[i][0])
    Ipr.append(Data[i][1])

# Function to calculate probe current
def probe_curr(P, x):
    return P[0]*((P[1]*(x-P[2]))+1 - np.exp((x-P[2])/P[3]))

# -----------------------------------------------------------
# fit until 8 volt (a bit before Vplasma) in steps of 0.2
Temp_list = []
while Vfin < 8:
    lim = 0
    for i in range(len(Vpr)):
        if Vpr[i] < Vfin:
            lim = i

    logdati = odr.Data(Vpr[:lim], Ipr[:lim])
    # Fit with previous parameters
    myodr = odr.ODR(logdati, odr.Model(probe_curr), beta0= [Isat, alfa, Vfl, Temp])
    myout = myodr.run()
    temper = myout.beta
    Isat=myout.beta[0]
    alfa=myout.beta[1]
    Vfl=myout.beta[2]
    Temp=myout.beta[3]
    Temp_list.append(Temp)   # register every Temp value

    #print("Vfin = " + str(Vfin)+ ". Isat = %f, alfa =%f Vfl = %f, Temp %f" % tuple(myout.beta))
    xar = np.arange(-40, 13, 0.1)
    plt.plot(Vpr, Ipr, '.', xar, probe_curr(myout.beta, xar), '-')

    Vfin=Vfin + 0.2


plt.savefig('fit_probecurr.jpg')
plt.clf()
#plt.show()

# calculating the interesting values
Vplasma=Vfl+3*Temp
errVpl= np.sqrt((myout.sd_beta[2]*myout.sd_beta[2])+9*(myout.sd_beta[3]*myout.sd_beta[3]))

ne= (-Isat)/(0.6*1.6e-19*2.5e-2*9.79e5*np.sqrt(Temp))/1e10
errne1= ((cost/np.sqrt(Temp))*(myout.sd_beta[0]))**2
errne2=(((cost*(-Isat))/(2*np.sqrt(Temp**3))*(myout.sd_beta[3])))**2
errne_tot= np.sqrt(errne1+errne2)

print ("Vplasma = {}, error = {}".format(Vplasma, errVpl))
print("Density = {}*10^10 cm^-3, error = {}*10^10 cm^-3".format(ne, errne_tot/1e10))
print("Electronic temperature = {}, error = {}".format(Temp, myout.sd_beta[3]))

# let's see the temperature
data = np.linspace(0, len(Temp_list), len(Temp_list))
plt.plot(data, Temp_list)
plt.savefig("temperature.jpg")
