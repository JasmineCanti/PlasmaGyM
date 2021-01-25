from scipy import
from pylab import
from scipy import
import numpy as N
import csv
from scipy import
*
*
optimize
stats
def c_s(T,Z,M):
return 9.79e3*sqrt(Z*T/M)
Opdec = 1.
RES = 4930
# Ion sound speed[m/s]
# 0.1
# Optical decoupler factor
# Resistenza
i=0
name=’namefile.txt’
# Inserire il nome del file da caricare
data=genfromtxt(name)
Vpr = data[:,1] - data[:,0]
Ipr = data[:,0]/4930
print ’Choose a maximum V value from the I-V plot to fit the ion saturation region’
print ’then close the plot’
figure()
plot(Vpr, Ipr,’r.’)
xlabel("Probe voltage [V]")
ylabel("Probe current [A]")
grid(True)
show()
55savefig("fit.png")
iord=Vpr.argsort()
Vord=Vpr[iord]
Iord=Ipr[iord]
Vpr=Vord
Ipr=Iord
VV = input("Enter the value [limit to fit Isat]:")
print ’then close the plot’
ii=where((Vpr-VV)<1e-16)
i1= size(ii) -1
figure()
a,b,R1,p1,std1 = stats.linregress(Vpr[0:i1], Ipr[0:i1])
plot(Vpr, Ipr,’r.’, Vpr,a*Vpr+b,’-’)
#print ’l intercetta e’, b
# Legend the plot
title(’raw data in linear scale’)
xlabel("Probe voltage [V]")
ylabel("Probe current [A]")
grid(True)
print ’R1 = ’,R1
print ’std1 = ’,std1
#print ’T = ’,p1[2]
#print ’alpha = ’,p1[3]
#print ’Vpl = ’, p1[1]+3.*p1[2]
show()
savefig("fit1.png")
print ’This is the electron current (Iprobe-Iion)’
Iel=Ipr-(a*Vpr+b)
figure()
plot(Vpr, Iel,’r.’)
title(’Ie’)
xlabel("Probe voltage [V]")
ylabel("Electron current [A]")
grid(True)
show()
savefig("fit2.png")
print ’This is the electron current in logarithmic scale ’
print ’Choose the voltage limits for the fitting procedure to obtain Te and Vplasma’
print ’’
figure()
plot(Vpr, Iel,’r.’)
56yscale(’log’)
ylim(1e-5,1e-1)
#xlim(-10,20)
title(’Log(Ie)’)
xlabel("Probe voltage [V]")
ylabel("Electron current [A]")
grid(True)
show()
savefig("fit3.png")
figure()
VV,WW,KK,KJ = input("Enter 4 numbers:")
im = where(Vpr<VV)
imm= where(Vpr<WW)
ikk= where(Vpr<KK)
ikj= where(Vpr<KJ)
i2 = size(im) -1
i3 = size(imm)-1
i4 = size(ikk)-1
i5 = size(ikj)-1
c,d,R2,p2,std2 = stats.linregress(Vpr[i2:i3], log(Iel[i2:i3]))
f,g,R3,p3,std3 = stats.linregress(Vpr[i4:i5], log(Iel[i4:i5]))
plot(Vpr, log(Iel),’r.’, Vpr,(c*Vpr+d),’-’,Vpr,(f*Vpr+g) ,’-’)
#yscale(’log’)
#ylim(1e-5,1e-1)
#xlim(-20,30)
title(’Log(Ie)’)
xlabel("Probe voltage [V]")
ylabel("Electron current [A]")
show()
savefig("fit4.png")
Aeff = 2.5e-6
me = 9.1e-31
mi = 1836.*me
q = 1.6e-19
Te = 1/c
Vplasma = (g-d)/(c-f)
Isat = a*Vpr[0]+b
print ’Te = ’,Te,’ [eV]’
print ’Vplasma = ’, Vplasma, ’ [V]’
print ’Isat = ’,Isat*1e3,’ [mA]’
ne = abs(Isat)/(0.6*q*sqrt(Te*q/mi)*Aeff)
print ’ne = ’,ne/1e16,’ [10^16 m-3]’
sigma_n = sqrt(pow(((std1/(0.6*q*Aeff)*sqrt(mi/Te))),2)+
+pow(((std2*Isat/(0.6*q*Aeff))*sqrt(mi/pow(Te,3))),2))
57print name
print ’R1 ’,’std1 ’,’R2 ’,’std2 ’,’R3 ’,’std3 ’,’Te ’,’Vpl ’,’Isat ’,
’ne[10^16 m-3] ’,’sigma_n’
print R1 ,std1 ,R2 ,std2 ,R3 ,std3,Te ,Vplasma ,Isat ,ne ,sigma_n
