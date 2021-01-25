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
flux=’30’
pot=’80’
name=’flusso30_pot80.txt’
data=genfromtxt(name)
#fittiamo i punti della pressione (Te*ne) con un polinomio
62fit=polyfit(data[:,0], data[:,1]*data[:,2], 5)
x=arange(-12,2,.1)
funzione=poly1d(fit)
y=funzione(x) #usiamo i punti ottenuti dal fit come nuovi dati
campo=diff(y, n=1, axis=-1) #calcoliamo il differenziale della pressione.
campo1=diff(data[:,1]*data[:,2], n=1, axis=-1)
#Mettiamo in un grafico i punti della pressione ottenuti ed il fit
figure()
plot(data[:,0],data[:,1]*data[:,2], ’bo’ )
plot(x, y, ’r’)
xlabel("posizione sonda (cm)")
ylabel("pressione(eV/cm^3)")
savefig("pressione.png")
grid(’on’)
#Stampiamo l’andamento della pressione.
figure()
plot(data[1:20,0], campo1, ’ro’)
fit=polyfit(data[1:20,0], campo1, 3)
grid(’on’)
xx=arange(-12,2,.1)
funzione=poly1d(fit)
yy=funzione(x)
plot(xx, yy, ’b’)
xlabel("posizione sonda (cm)")
ylabel("Gradiente Pressione (eV/cm^4)")
title("gradiente pressione flusso "+flux+" potenza"+pot+" %")
savefig("profilopressione-flux"+flux+"pot"+pot+".png")
