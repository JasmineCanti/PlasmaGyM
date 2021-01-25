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
flux=’10’
pot=’80’
name=’pot_80.txt’
data=genfromtxt(name)
#Fittiamo il potenziale con un polinomio
fit=polyfit(data[:,0], data[:,3], 3)
x=arange(-12,2,.1)
funzione=poly1d(fit)
y=funzione(x)
#usiamo il fit ottenuto per avere piu punti dei 20 analizzati
campo=-diff(y, n=1, axis=-1) #calcoliamo il campo elettrico come -gradiente(V)
ii=5 #scegliamo fino a che punto fittare con una retta la salita
xii=-8.
61#Fittiamo la salita linearmente
flin=polyfit(data[:ii,0], data[:ii,3], 1)
xx=arange(-12,xii,.1)
fnzlin=poly1d(flin)
yy=fnzlin(xx)
#Facciamo un primo grafico con i punti del Vplasma calcolato e i 2 fit ottenuti sopra
figure()
errorbar(data[:,0], data[:,3], yerr=data[:,6], fmt=’bo’)
plot(x, y, ’r’, label=’fit’)
legend()
xlabel("posizione sonda (cm)")
ylabel("Vplasma (V)")
title("Potenziale di plasma - flusso "+flux+" potenza "+pot+"%")
plot(xx,yy)
savefig("profiloelettrico-flux "+flux+"pot"+pot+".png")
#calcoliamo poi campo elettrico medio nella salita e velocita di drift
print ’pot [%] ’,pot, ’ flux [sccm] :’,flux
print ’Campo El [V/m]:’, flin[0]/(xx[0]-xii)/1e-2
print ’vdrift [m/s]:’, flin[0]/(xx[0]-xii)/(70.e-3)/1e-2
#Stampiamo l’andamento del campo elettrico
figure()
plot(x[1:140],campo, ’b’)
grid()
xlabel("posizione sonda (cm)")
ylabel("campo elettrico (V/cm)")
title("profilo flusso"+flux+" potenza "+pot+"%")
savefig("profilocampo-flux "+flux+"pot"+pot+".png")
