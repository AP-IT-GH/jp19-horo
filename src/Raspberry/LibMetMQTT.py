from __future__ import division
from time import sleep
import math
import paho.mqtt.client as paho
import numpy

import Adafruit_PCA9685

CONST_PI = 3.14159265359
CONST_HALFPI = 1.5707963268
CONST_DOUBLE_PI = 6.28318530718
CONST_DEGREE_STEP = 0.01745329251
CONST_FREE_ANGLE = 999.9

step_base = 350;
step_shoulder = 350;
step_elbow = 350;
step_wrist_ver = 350;
step_wrist_rot = 350;
step_gripper = 350;

PINNRBASE = 0
PINNRELBOW = 11
PINNRSHOULDER = 7
PINNRWRISTVER = 15
PINNRWRISTROT = 4
PINNRGRIPPER =5

baseCheck = False
shoulderCheck = False
verwristCheck = False
ElbowCheck = False
rotwristCheck = False
gripCheck = False

a0=0.0
a1=0.0
a2=0.0
a3=0.0

pwm = Adafruit_PCA9685.PCA9685()
servo_min = 85 
servo_max = 515 

#515 - 85 = 430 range van servo

MQTTRECEIVED = False

client = paho.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.connect("192.168.0.69", 1883)

paho.Client(client_id="", clean_session=True, userdata=None, protocol= paho.MQTTv31)
client.loop_start()
pwm.set_pwm_freq(45.32)


def on_connect(client, userdata, flags,rc):
    print("connack received with code %d." % (rc))

def on_publish(client, mid, msg):
    print(msg.payload)
    
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    MQTTRECEIVED=False


def set_servo_pulse(channel, pulse):
	pulse_length = 1000000    # 1,000,000 us per second
	pulse_length //= 60       # 60 Hz
	print('{0}us per period'.format(pulse_length))
	pulse_length //= 4096     # 12 bits of resolution
	print('{0}us per bit'.format(pulse_length))
	pulse *= 1000
	pulse //= pulse_length
	pwm.set_pwm(channel, 0, pulse)

class Link:
	_length=0.0
	_anglelow=0.0
	_anglehigh=0.0
	_angle=0.0

	def init(self,length,angle_low_limit,angle_high_limit):
		self._length = length
		self._anglelow = angle_low_limit
		self._anglehigh = angle_high_limit

	def inRange(self,angle):
		
		#print("LOW:" + str(self._anglelow))
		#print("ANGLE" + str(angle))
		#print("ANGLEHIGH:" + str(self._anglehigh))
		return ((angle >= self._anglelow) and (angle <= self._anglehigh))

	def getLength(self):
		return self._length

	def getAngle(self):
		return self._angle

	def setAngle(self, angle):
		self._angle = angle


class Inverse:
	_L0 = Link()
	_L1 = Link()
	_L2 = Link()
	_L3 = Link()

	gamma = 0.0
	beta = 0.0

	_CurrentPhi = 0

	def __init__(self):
		_CurrentPhi = -CONST_DOUBLE_PI

	def attach(self,Shoulder,UpperArm,Forearm,Hand):
		self._L0 = Shoulder
		self._L1 = UpperArm
		self._L2 = Forearm
		self._L3 = Hand

	def solve():
		pass

	def CosRule(self,opposite,adjacent1,adjacent2,angle):

		delta = 2 * adjacent1 * adjacent2

		if(delta == 0):
			return false

		cos = (adjacent1*adjacent1 + adjacent2*adjacent2 - opposite*opposite) / delta

		if((cos > 1) or (cos < -1)):
			return False

		angle = math.acos(cos)

		return (angle)

	# Inverse solve functie
	def _solve(self,x, y, phi, shoulder, elbow, wrist):
		global CONST_HALFPI
		global CONST_PI
		global a1
		global a2
		global a3
		
		

		_r = math.sqrt(x*x + y*y)
		_theta = math.atan2(y, x)
		_x = _r * math.cos(_theta - CONST_HALFPI)
		_y = _r * math.sin(_theta - CONST_HALFPI)
		_phi = phi - CONST_HALFPI

		# Coordinate for the wrist
		xw = _x - self._L3.getLength() * math.cos(_phi)
		yw = _y - self._L3.getLength() * math.sin(_phi)

		# Get polar system
		alpha = math.atan2(yw, xw)
		R = math.sqrt(xw*xw + yw*yw)

		#  Calculate inner angle of the shoulder
		beta = 0.0
		if (not(self.CosRule(self._L2.getLength(), R, self._L1.getLength(), beta))):
			return False
		else:
			beta =  self.CosRule(self._L2.getLength(), R, self._L1.getLength(), beta)

		# Calculate the inner angle of the elbow
		gamma =0.0
		if (not(self.CosRule(R, self._L1.getLength(), self._L2.getLength(), gamma))):
			return False
		else:
			gamma =  self.CosRule(R, self._L1.getLength(), self._L2.getLength(), gamma)

		# Solve the angles of the arm
		_shoulder = alpha - beta
		_elbow = CONST_PI - gamma
		_wrist = _phi - _shoulder - _elbow


		# Check the range of each hinge
		if not(self._L1.inRange(_shoulder)) or not(self._L2.inRange(_elbow)) or not(self._L3.inRange(_wrist)):
			# If not in range, solve for the second solution
			
			_shoulder += 2 * beta
			_elbow *= -1
			_wrist = _phi - _shoulder - _elbow

			# Check the range for the second solution
			if ((not(self._L1.inRange(_shoulder))) or (not(self._L2.inRange(_elbow))) or (not(self._L3.inRange(_wrist)))):
				return False
		# Return the solution
		shoulder = _shoulder
		elbow = _elbow
		wrist = _wrist
		a1 = shoulder
		a2 = elbow
		a3 = wrist

		return True

	def _solveFr(self,x,y,shoulder,elbow,wrist):
		if(self._solve(x,y,self._CurrentPhi,shoulder,elbow,wrist)):
			return True

		PhI = -CONST_DOUBLE_PI
		while PhI < CONST_DOUBLE_PI:
			if(self._solve(x,y,PhI,shoulder,elbow,wrist)):
				self._CurrentPhi=PhI
				return True

			PhI = PhI+CONST_DEGREE_STEP

		return False
			




	def Solve(self,x,y,z,base,shoulder,elbow,wrist,*phi):
		#Berekenen in welke richting de Base servo moet staan voor in het juiste kwadrant te staan
		_r = math.sqrt(x*x + y*y)
		_base = math.atan2(y,x)
		_base = round(_base,2)
		Phi= phi[0]
		global a0

		#als base niet juist staat, base omdraaien naar ander kwadrant
		if(not(self._L0.inRange(_base))):
			#_base += (_base < 0) ? PI : -PI
			if(_base+_base < 0):
				_base = _base + CONST_PI
			else:
				_base = _base - CONST_PI
			_r = _r*-1

			if(Phi != CONST_FREE_ANGLE):
				Phi = CONST_PI - Phi
		_PHI = Phi

		#Als via ingesteld Phi hoek niet mogelijk is, kijken of zonder ingestelde hoek wel bereikbaar is
		if(not(self._solve(_r,z- self._L0.getLength(),_PHI,shoulder,elbow,wrist))):
			if(not(self._solveFr(_r,z- self._L0.getLength(),shoulder,elbow,wrist))):
				return False

		#A0 op berekende positie zetten
		base = _base
		a0 = _base
		return True









#fUNCTIE OM ALLE SERVOS TE BESTUREN
def BraccioMovement(stepdelay, vBase, vShoulder, vElbow, vWrist_ver,vWrist_rot,vGripper ):
	global step_base
	global step_gripper
	global step_shoulder
	global step_wrist_rot
	global step_wrist_ver
	global step_elbow

	global baseCheck
	global shoulderCheck
	global verwristCheck
	global ElbowCheck 
	global rotwristCheck
	global gripCheck

	baseCheck = False
	shoulderCheck = False
	verwristCheck=False
	ElbowCheck = False
	rotwristCheck=False
	gripCheck=False

	global PINNRBASE
	global PINNRELBOW
	global PINNRSHOULDER
	global PINNRWRISTVER 
	global PINNRWRISTROT
	global PINNRGRIPPER

	print("Vbase : " + str(vBase))
	print("vShoulder : " + str(vShoulder))
	print("VElbow : " + str(vElbow))
	print("vWrist_ver : " + str( vWrist_ver))

	vBase = Checkvalue(0,180,vBase)
	vElbow = Checkvalue(15,165,vElbow)
	vShoulder = Checkvalue(15,165,vShoulder)
	vWrist_ver = Checkvalue(15,165,vWrist_ver)
	vWrist_rot = Checkvalue(15,165,vWrist_rot)
	vGripper = Checkvalue(10,73,vGripper)

	print("vBase : " + str(vBase))

	exit = 1
	




	while(exit):

		step_base=Servosteps(vBase,step_base,PINNRBASE)
		step_shoulder = Servosteps(vShoulder,step_shoulder,PINNRSHOULDER)
		step_gripper = Servosteps(vGripper,step_gripper,PINNRGRIPPER)
		step_elbow = Servosteps(vElbow,step_elbow,PINNRELBOW)
		step_wrist_rot = Servosteps(vWrist_rot,step_wrist_rot,PINNRWRISTROT)
		step_wrist_ver = Servosteps(vWrist_ver,step_wrist_ver,PINNRWRISTVER)

		

		sleep(stepdelay/1000)
		
		
		if ((baseCheck) and (shoulderCheck) and (gripCheck) and (ElbowCheck) and (rotwristCheck) and (verwristCheck)):
			exit = 0

def Servosteps(A,B,C):
	#PWM voor servo stappen te zetten, Checks om te zien of hij op finale positie staat
	global pwm
	global baseCheck
	global shoulderCheck
	global verwristCheck
	global ElbowCheck 
	global rotwristCheck
	global gripCheck

	#zit servo in range van gewilde waarde met maxium 2,38 ertussen? zet servo op finale positie
	if(A  > B-2.38 and A < B+2.38):
		B = A
		if(C == PINNRBASE):
			baseCheck = True
		elif(C == PINNRSHOULDER):
			shoulderCheck = True
		elif(C == PINNRGRIPPER):
			gripCheck = True
		elif(C == PINNRELBOW):
			ElbowCheck = True
		elif(C == PINNRWRISTROT):
			rotwristCheck = True
		elif(C == PINNRWRISTVER):
			verwristCheck = True

	#is servo huidge positie groter dan gewilde positie -> servo waarde hoger
	if(A > B):
		B = B+2.38
	#is servo huidge positie kleiner dan gewilde positie -> servo waarde lager
	elif(A < B):
		B = B-2.38
	#Effectief de servo positie aanpassen
	pwm.set_pwm(C, 0, int(B))

	#huidige positie terug geven
	return B

def Checkvalue(ParamMin,ParamMax,Param):
	if(Param > ParamMax):
		Param = ParamMax
	elif(Param < ParamMin):
		Param = ParamMin
	return (Param*2.388888888) + 85

def b2a(b):
	return b /180.0 * CONST_PI - CONST_HALFPI

def a2b(a):
	return ( a + CONST_HALFPI) * 180/ CONST_PI

#Servo's op een start positie zetten die veilig is om te starten
pwm.set_pwm(PINNRBASE, 0, 350)
pwm.set_pwm(PINNRELBOW, 0, 350)
pwm.set_pwm(PINNRSHOULDER, 0, 350)
pwm.set_pwm(PINNRWRISTVER, 0, 350)

#Links aanmaken
base = Link()
upperarm = Link()
forearm = Link()
hand = Link()
InverseK = Inverse()

	

	#initializeren met lengte, minimum hoek en maximum hoek
base.init(0,b2a(0.0),b2a(180.0))
upperarm.init(200,b2a(15.0),b2a(165.0))
forearm.init(200,b2a(0.0),b2a(180.0))
hand.init(270,b2a(0.0),b2a(180.0))

#Links aan InverseK library binden
InverseK.attach(base,upperarm,forearm,hand)

while True:
	print "yeet"
	if MQTTRECEIVED:
		#Bereken via library of deze coordinaten bereikbaar zijn
		if(InverseK.Solve(Xcoord,Ycoord,Zcoord,a0,a1,a2,a3,0.0)):
			print("Possible")
			#effectief de servos zetten op de berekende servo waardes
			BraccioMovement(20,a2b(a0),a2b(a1),a2b(a2),a2b(a3),Kracht,Hoek)
		else:
			print("Out of Reach")
	
	sleep(5)

	

	
