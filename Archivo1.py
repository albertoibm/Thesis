from time import sleep,time
from sys import stdout,exit,argv
import pygame
from pygame.locals import *
from math import sin,cos,pi,sqrt
import getnavdata_conf as cnf

grados=pi/180

class Ventana:   ### PyGame Window
	def __init__(self,screen,drone):
		self.screen = screen
		self.panel = load_image(cnf.img_panel,1)
		self.img = load_image(cnf.img_compass)
		self.size = cnf.size
		self.pos = cnf.position
		self.p=cnf.horizon
		self.position=[]
		self.b=cnf.compass_vector	##compass needle vector
		self.bp=cnf.compass_angle	##compass needle angle
		self.h=cnf.altitude_vector
		self.hp=cnf.altitude_angle
		self.drone=drone

	def draw(self,ph,th,ps,alt):
		self.loadPosition(ph*grados,th*grados,ps*grados,alt)
		pygame.draw.rect(self.screen,Color(cnf.background_color),\
				(cnf.background_rect))
                if '-v' not in argv:
			camera = pygame.image.fromstring("\x00\x00\x00"*\
			cnf.cam_size[0]*cnf.cam_size[1],cnf.cam_size, 'RGB')
		else:
			camera = pygame.image.fromstring(drone.image, cnf.drone_cam, 'RGB')
                if cnf.drone_cam != cnf.cam_size:
                        camera = pygame.transform.scale(camera,cnf.cam_size)
                self.screen.blit(camera, cnf.cam_pos)
		pygame.draw.circle(self.screen,Color('cyan'),self.pos,70)
		pygame.draw.polygon(self.screen,Color('brown'),tuple(self.position))
		self.screen.blit(self.panel,cnf.pos_panel)
		pygame.draw.line(self.screen,Color('red'),self.transform((0,0),\
				cnf.pos_compass),self.bp,2)
		pygame.draw.line(self.screen,Color('white'),self.transform((0,0),\
				cnf.pos_altimeter),self.hp,2)

		Instrucciones="Controles: "
                Instrucciones+="a: Mover a la izquierda; "
                Instrucciones+="s: Mover hacia atras; "
                Instrucciones2="d: Mover a la derecha; "
                Instrucciones2+="w: Mover hacia adelante"
                Instrucciones3="Flecha izquierda/derecha: Girar izquierda/derecha; "
                Instrucciones4="Flecha arriba/abajo: Subir/Bajar"
                if usedrone:
			PositionText="Altitud: %.2fm | Bateria: %d%% "%(alt,drone.navdata[0]['battery'])
		else:
			PositionText=""
                
                f=pygame.font.Font(None,15)
                hudInstrucciones=f.render(Instrucciones,True,cnf.color_instruc)
                hudInstrucciones2=f.render(Instrucciones2,True,cnf.color_instruc)
		hudInstrucciones3=f.render(Instrucciones3,True,cnf.color_instruc)
		hudInstrucciones4=f.render(Instrucciones4,True,cnf.color_instruc)
                f=pygame.font.Font(None,15)
                hudPosition=f.render(PositionText,True,cnf.color_instruc)
                screen.blit(hudInstrucciones,cnf.pos_instruc)
                screen.blit(hudInstrucciones2,cnf.pos_instruc2)
		screen.blit(hudInstrucciones3,cnf.pos_instruc3)
                screen.blit(hudPosition,cnf.pos_altura)
		pygame.display.update()

	def loadPosition(self,ph,th,ps,alt):
		self.position=[]
		for p in self.p:
			self.position.append(tuple(p))
		self.position[0]=[self.position[0][0],self.position[0][1]-th*10/(2*pi)]
		self.position[1]=[self.position[1][0],self.position[1][1]-th*10/(2*pi)]
		self.position[0]=(self.position[0][0]*cos(ph)-self.position[0][1]*\
				sin(ph),self.position[0][0]*sin(ph)+\
				self.position[0][1]*cos(ph))
		self.position[1]=(self.position[1][0]*cos(ph)-self.position[1][1]*\
				sin(ph),self.position[1][0]*\
				sin(ph)+self.position[1][1]*cos(ph))
		self.position=map(self.transform,self.position)
		self.bp=(self.b[0]*cos(ps)-self.b[1]*sin(ps),self.b[0]*sin(ps)+\
				self.b[1]*cos(ps))
		self.bp=self.transform(self.bp,cnf.pos_compass)
		angh = pi/2-2*pi*alt/5
		self.hp=(self.h[0]*cos(angh)-self.h[1]*sin(angh),self.h[0]*\
			sin(angh)+self.h[1]*cos(angh))
		self.hp=self.transform(self.hp,cnf.pos_altimeter)

	def transform(self,x,pos=cnf.position):
		return (x[0]*self.size+pos[0],pos[1]-x[1]*self.size)

def load_image(file,a=0):
        try:
                img = pygame.image.load(file)
        except:
                exit("No se pudo cargar la imagen %s"%file)
        if not a:return img.convert()
        return img.convert_alpha()


## INICIO
savedata = True if '--save-data' in argv else False
usedrone = True if '--no-drone' not in argv else False
if '-h' in argv:
	print "Opciones:"
	print "--save-data\tGuarda los datos recogidos en data-mano.txt"
	print "--no-drone\tDesactiva el uso del AR.Drone"
	print "-v\tActiva el video (camaras)"
	exit()

if usedrone:
	import libardrone
	drone=libardrone.ARDrone()
	sleep(2)
	drone.zap(libardrone.ZAP_CHANNEL_LARGE_HORI_SMALL_VERT)
else:
	drone=None

### GET NAV DATA EXPERIMENTO
if savedata:
	archivo=open('data-vuelo.txt','w')

if usedrone:
	sleep(2)
	drone.reset()
	sleep(1)
	drone.trim()

pygame.init()
screen = pygame.display.set_mode((cnf.width,cnf.height))
ventana = Ventana(screen,drone)
th,ph,ps=-10,15,90
alt=0
t0=time()
Escape=False
flying = False
tmp=th
dt=0
ta=t0
print "Todo listo!"
while not Escape and not (flying and time()-t0 > 10):
	for e in pygame.event.get():
		if e.type==pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				Escape = True
			elif e.key == pygame.K_RETURN:
				t0 = time()
				flying = True
				drone.takeoff()
			elif e.key == pygame.K_SPACE:
				flying = False
				drone.land()
			elif e.key == pygame.K_BACKSPACE:
				flying = False
				drone.reset()
			elif e.key == pygame.K_a:
				drone.move_left()
			elif e.key == pygame.K_s:
				drone.move_backward()
			elif e.key == pygame.K_d:
				drone.move_right()
			elif e.key == pygame.K_w:
				drone.move_forward()
			elif e.key == pygame.K_UP:
				drone.move_up()
			elif e.key == pygame.K_DOWN:
				drone.move_down()
			elif e.key == pygame.K_LEFT:
				drone.turn_left()
			elif e.key == pygame.K_RIGHT:
				drone.turn_right()
	if usedrone:
		th=drone.navdata[0]['theta']
		ph=drone.navdata[0]['phi']
		ps=drone.navdata[0]['psi']
		alt=drone.navdata[0]['altitude']/1000.0
	if th!=tmp:
		dt=time()-ta
		ta=time()
		tmp=th
	if savedata:
		archivo.write("%.4f,%.2f,%.2f,%.2f,%.2f,%.4f\n"%(time()-t0,alt,th,ph,ps,dt))
	ventana.draw(ph,th,ps,alt)
print "Cerrando"
pygame.display.quit()
drone.land()
sleep(3)
if savedata:
	archivo.close()
if usedrone:
	drone.halt()
exit()
