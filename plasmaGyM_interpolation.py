from scipy import
from pylab import
from scipy import
import numpy as N
import csv
from scipy import
from scipy import
*
*
optimize
stats
interpolate
name=’pot_20.txt’
data=genfromtxt(name)
n=4

# Grado del polinomio del fit
# Fit temperatura
fit=polyfit(data[:,0], data[:,1], n)
x=arange(-12,2,.1)
funzione=poly1d(fit)
y=funzione(x)
figure()
errorbar(data[:,0], data[:,1], yerr=data[:,4], fmt=’bo’)
plot(x, y, ’r’)
xlabel("posizione sonda (cm)")
ylabel("Te (eV)")
title("Te-pos flusso 10 pot 20")
savefig("Te-pos10pot20.png")

# Fit densita
fit=polyfit(data[:,0], data[:,2], n)
x=arange(-12,2,.1)
funzione=poly1d(fit)
y=funzione(x)
figure()
errorbar(data[:,0], data[:,2], yerr=data[:,5], fmt=’bo’)
plot(x, y, ’r’)
xlabel("posizione sonda (cm)")
ylabel("ne (10^10 cm^-3)")
title("ne-pos flusso 10 pot 20")
58savefig("ne-pos10pot20.png")

# Fit Vplasma
fit=polyfit(data[:,0], data[:,3], n)
x=arange(-12,2,.1)
funzione=poly1d(fit)
y=funzione(x)
figure()
errorbar(data[:,0], data[:,3], yerr=data[:,6], fmt=’bo’)
plot(x, y, ’r’)
xlabel("posizione sonda (cm)")
ylabel("Vplasma (V)")
title("Vplasma-pos flusso 10 pot 20")
savefig("Vplasma-pos10pot20.png")
