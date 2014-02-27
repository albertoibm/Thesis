import libardrone
import  numpy
from time import time,sleep
from sys import stdout,exit,argv
from math import sqrt,pi
from PID import PID
import diffOrdN

GRADOS=pi/180

class Integral:
	""" Calcula la integral de una funcion dada como parametro"""
	def __init__(self,f):
		self.f=f
		self.integral=0.
		self.val=0.
	def update(self,x,dt):
		self.integral+=(self.f(x)+self.val)/2*dt
		self.val=self.f(x)

ttotal=10 ## Tiempo total de vuelo
factor=1

### Parametros del controlador
delta=numpy.matrix(numpy.diag([12,12,8]))
K1=4.5*numpy.sqrt(delta)
K2=1.1*delta
lamda=numpy.matrix(numpy.diag([3,3,3]))

### Parametros del cuadricoptero
l=0.13
Ixx=24.1e-3
Iyy=23.2e-3
Izz=45.1e-2
b=0.0006646195542576290
b=0.000064601020673842

d=b*9.72


## Matriz de inercia y su inversa
g=numpy.matrix(numpy.diag([l/Ixx,l/Iyy,1/Izz]))
ginv=g.I

## Vectores de x deseada y su derivada
xd=numpy.array([[0],[0],[0]])
xpd=numpy.array([[0],[0],[0]])
Altd=260

## Objeto diferenciador numerico por modos deslizantes
difN = 4 ## Orden del diferenciador
dif = diffOrdN.DiffOrdN(difN,[12,8,4,3.5,2.1])

## Objeto que calcula la integral de la funcion signo 
intsgn=Integral(lambda x:numpy.sign(x))
## Controlador de altitud
ctrlalt=PID(.7,.2,.1)

### Se establece configuracion con el ardrone, se apagan los motores y se cambia el modo de camara
stdout.write("Estableciendo comunicacion con el ARDrone\n")
stdout.flush()
drone=libardrone.ARDrone()
sleep(1)
print "Listo!"
stdout.write("Estableciendo configuracion inicial\n")
stdout.flush()
drone.reset()
sleep(0.1)
drone.trim()
sleep(1.5)
drone.reset()
print "Encendiendo motores"
drone.pwm(1,1,1,1)
sleep(5)
drone.zap(libardrone.ZAP_CHANNEL_LARGE_HORI_SMALL_VERT)
sleep(0.1)
print "Listo!"


## Vectores para guardar datos de vuelo
angs=[]
us=[]
oms=[]
ts=[]

## define el tiempo inicial
ta=time()
t0=ta
xa=0

while time()-t0<ttotal:
	dt = -ta + time()
	ta = time()
	Alt = 260#drone.navdata[0]['altitude']
	Th = drone.navdata[0]['theta']*GRADOS
	Ph = drone.navdata[0]['phi']*GRADOS
	Ps = drone.navdata[0]['psi']*GRADOS
	x = numpy.matrix([[Th],[Ph],[Ps]])  
	dif.update(x,dt)
	o = dif.output()
	x = o[difN]
	xp = o[difN-1]
#	xp = (x - xa)/dt
	xa = x+0
	e = xd-x
	ep = xpd-xp
	s = ep+lamda*e
	intsgn.update(s,dt)
	u = -lamda*ep-\
	K1*numpy.matrix(numpy.array(numpy.sqrt(numpy.abs(s)))*numpy.array(numpy.sign(s)))\
	-K2*intsgn.integral
	u = ginv*u
	om1=om2=om3=om4 = 0
	U4 = max(0,ctrlalt.sal(Altd-Alt,dt))

	try:om1=int(round(sqrt(-(b*u[2]+d*u[0]-d*U4+d*u[1])/(4*b*d))*factor))
	except:pass
	try:om2=int(round(sqrt((-d*u[0]+d*u[1]+b*u[2]+d*U4)/(4*b*d))*factor))
	except:pass
	try:om3=int(round(sqrt(-(-d*u[1]+b*u[2]-d*U4-d*u[0])/(4*b*d))*factor))
	except:pass
	try:om4=int(round(sqrt((d*U4+b*u[2]+d*u[0]-d*u[1])/(4*b*d))*factor))
	except:pass
	om1=10+om1 if om1<10 else om1
	om2=10+om2 if om2<10 else om2
	om3=10+om3 if om3<10 else om3
	om4=10+om4 if om4<10 else om4
        stdout.write("\b"*100+"(%.2f,%.2f,%.2f,%.2f)"%(U4,u[0],u[1],u[2]))
        stdout.write("\b"*0+"|[%.2f,%.2f,%.2f,%.2f]"%(om1,om2,om3,om4))
        stdout.write("{%.4f}    "%dt)
        stdout.flush()
	if "-p" not in argv:
		drone.pwm(om1,om2,om3,om4)
	angs.append([x[0][0],x[1][0],x[2][0]]) ## Th,Ph,Ps
	us.append([U4,u[0],u[1],u[2]])
	oms.append([om1,om2,om3,om4])
	ts.append(time()-t0)
drone.pwm(0,0,0,0)
drone.halt()
print ""
archivo=open("res_supertwisting.txt",'w')
for i in range(len(ts)):
	archivo.write("%.3f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"%\
		(ts[i],angs[i][0],angs[i][1],us[i][0],us[i][1],us[i][2],\
		us[i][3],oms[i][1],oms[i][2],oms[i][3]))
archivo.close()
exit()
