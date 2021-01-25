from scipy import
from pylab import
from scipy import
import numpy as N
import csv
from scipy import
Ampl = 7.41
RES = 1000
*
*
optimize
stats
# Fattore di amplificazione
# Resistenza
i=0
name=’namefile’
# Inserire il nome del file da caricare
data=genfromtxt(name)
Vpr = data[0:5000,2]*Ampl
Ipr = data[0:5000,3]/RES
# Teniamo in considerazione la capacita parassita
# Aggiungendola alle discese del segnale e aggiungendole alle salite.
for i in range(1, 4999):
if Vpr[i] < Vpr[i+1]:
Ipr[i] = Ipr[i] - 1.5e-5
else:
Ipr[i] = Ipr[i] + 1.5e-5
Vpr = Vpr-RES*Ipr
59Vfin=2
#valore fino a cui il programma fitta
# Valori iniziali dei parametri dei fit
Isat=-0.0002
Vfl=5
Temp=4.
alfa=1.
# Ordiniamo i dati per poterli analizzare ad intervalli.
Dati = zip(*sorted(zip(Vpr, Ipr)))
Vpr=Dati[:][0]
Ipr=Dati[:][1]
aa=[]
costante=4.256e14
j=0
while Vfin<8:
# Aumentiamo il fit sino a raggiungere 8 V
for i in range (1, 4999):
#(poco prima del Vplasma) a intervalli di 0.2 V
if Vpr[i]<Vfin:
lim=i
figure()
import scipy.odr as odr
def funzione(P, x):
return P[0]*((P[1]*(x-P[2]))+1 - exp((x-P[2])/P[3]))
logdati = odr.Data(Vpr[0:lim], Ipr[0:lim])
# Fit utilizzando i parametri ottenuti in precedenza
myodr = odr.ODR(logdati, odr.Model(funzione), beta0= [Isat, alfa, Vfl, Temp])
myout = myodr.run()
temper = myout.beta
Isat=myout.beta[0]
alfa=myout.beta[1]
Vfl=myout.beta[2]
Temp=myout.beta[3]
grid(True)
aa.append(Temp)
j=j+1
print "Isat = %f, alfa =%f Vfl = %f, La temperatura e’ %f" % tuple(myout.beta)
# Stampa i valori ad ogni fit
xarr = arange(-40, 13, .1)
plot(Vpr, Ipr, ’r-’, xarr, funzione(myout.beta, xarr))
savefig("fitodr.png")
Vfin=Vfin+ 0.2
60Vplasma=Vfl+3*Temp
print "Vplasma= ", Vplasma
ne= (-Isat)/(0.6*1.6e-19*2.5e-2*9.79e5*sqrt(Temp))/1e10
print "densita= ", ne, "*10^10 cm^-3"
errVpl= sqrt((myout.sd_beta[2]*myout.sd_beta[2])+
+9*(myout.sd_beta[3]*myout.sd_beta[3]))
print "l’errore su vpl:", errVpl
errparte1= ((costante/sqrt(Temp))*(myout.sd_beta[0]))**2
errparte2=(((costante*(-Isat))/(2*sqrt(Temp**3))*(myout.sd_beta[3])))**2
errne= sqrt(errparte1+errparte2)
print "l’errore su ne:", errne/1e10, "*10^10 cm^-3"
print "l’errore su te:", myout.sd_beta[3]
# Vediamo l’andamento della temperatura su tutti i fit.
xx=linspace(0,len(aa),len(aa))
figure()
plot(xx,aa)
savefig("AndamentoTemperatura.png")
print Temp, ne, Vplasma, myout.sd_beta[3], errne/1e10, errVpl
