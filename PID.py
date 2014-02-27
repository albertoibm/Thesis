from time import time
class PID:
        def __init__(self,kp=1,ki=0,kd=0,h=0.01):
                self.t=time()
                self.kp=float(kp)
                self.ki=float(ki)
                self.kd=float(kd)
                self.h=h
                self.I=0
                self.d0=0
                self.D=0
		print "Controlador creado"
		print "kP=",self.kp
		print "kI=",self.ki
		print "kD=",self.kd
        def sal(self,e,dt):
                tScale=1
                self.dt=dt
                self.t=time()
                self.I+=(e-self.d0)/2*self.dt+self.dt*self.d0
                self.D=(-self.d0+e)/self.dt
		if self.D>100:self.D=100
		elif self.D<-100:self.D=-100
                self.d0=e
                return self.kp*e+self.ki*self.I+self.kd*self.D

