from numpy import sign as sgn
from numpy import power,array as arry
class DiffOrdN:
	def __init__(self,n,gains):
		self.orden = n
		self.diffs = []
		for i in range(n+1):
			self.diffs.append(Diff(i,gains[-(i+1)]))
	def update(self,val,dt):
		zm1=0
		for i in range(self.orden,-1,-1):
			if i == 0: zm1 = 0
			else:
				zm1 = self.diffs[i-1].output()
			self.diffs[i].trnsFnc(val,zm1)
			val=self.diffs[i].value()
			self.diffs[i].integrate(val,dt)
	def output(self,d=0):
		## d es el orden de la derivada que se desea obtener
		outs=[]
		for i in range(self.orden+1):
			outs.append(self.diffs[i].output())
		return outs
		
class Diff:
	def __init__(self,n,G):
		self.orden=float(n)
		self.integral=0
		self.gain=G
		self.tmp=0
		self.preintval=0
		print "Orden creado: %d, Ganancia %.2f"%(n,G)
	def trnsFnc(self,entrada,zm1):
		self.preintval=-arry(sgn(self.integral-entrada)*self.gain)*arry(power(abs(self.integral-entrada),potencia(self.orden)))+zm1
	def value(self):
		return self.preintval
	def output(self):
		return self.integral
	def integrate(self,val,dt):
		self.integral+=(val+self.tmp)*dt/2.0
		self.tmp=val
def potencia(n):
	return n/(n+1)
