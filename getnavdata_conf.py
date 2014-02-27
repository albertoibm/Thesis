### ARCHIVO DE CONFIGURACION DE getnavdata
### INTERFAZ GRAFICA PARA USO DEL AR.Drone
from pygame import Rect
width=640
height=700
img_panel="panel_helicopter.png"
pos_panel=(104,392)
img_compass="compass.jpg"
pos_compass=(322,468)
pos_altimeter=(463,463)
size=30
position=(180,465)
horizon=[]
horizon.append([-2.2,0])
horizon.append([2.5,0])
horizon.append([3,-.6])
horizon.append([1.4,-2.2])
horizon.append([-1.4,-2.2])
horizon.append([-2.3,-.3])
compass_vector=[1.4,0.0]
compass_angle=9.0
altitude_vector=[1.4,0.0]
altitude_angle=9.0
background_color='black'
background_rect=(0,0,width,height)
cam_size=(640,480)#320,240)
drone_cam=(320,240)
cam_pos=(0,0)
color_instruc=(0,200,0)
pos_instruc=(120,575)
pos_instruc2=(120,590)
pos_instruc3=(120,605)
pos_instruc4=(120,620)
pos_altura=(180,650)
color_motor=(0,164,250)
vals_motor=[150,50,250,50]
motor_y=670
pos_motor1=Rect(430,motor_y-int(139*vals_motor[0]/511.),\
	18,int(139*vals_motor[0]/511.))
pos_motor2=Rect(450,motor_y-int(139*vals_motor[1]/511.),\
	18,int(139*vals_motor[1]/511.))
pos_motor3=Rect(470,motor_y-int(139*vals_motor[2]/511.),\
	18,int(139*vals_motor[2]/511.))
pos_motor4=Rect(490,motor_y-int(139*vals_motor[3]/511.),\
	18,int(139*vals_motor[3]/511.))

