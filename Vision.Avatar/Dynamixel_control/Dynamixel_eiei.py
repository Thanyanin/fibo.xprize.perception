import paho.mqtt.client as mqtt
from dynamixel_control import Dynamixel
from math import atan2,sqrt,degrees

host = "192.168.1.186"
port = 1883

# host = "broker.mqttdashboard.com"
# port = 8000
portDynamixel = Dynamixel('COM6',1000000)
portDynamixel.connect()
motor_type = 'Ax'

def m(ID, position):
    portDynamixel.setDeviceMoving(ID, motor_type, position, 1023, 1023)#ID, type, goal position, goal speed, max torque
def p(ID):
    return portDynamixel.getMotorPosition(ID)

DynamixelposID3 = p(3)
DynamixelposID2 = p(2)
DynamixelposID12 = p(12)
DynamixelgoalposID3 = p(3)
DynamixelgoalposID2 = p(2)
DynamixelgoalposID12 = p(12)

def Z_axis(value): # 205 . 819 น้อยเอียงซ้าย
    value = float(value)
    roll = 512
    if int(value) in range(270, 360):
        roll = (512 + ((value-360) * 3.4))
    elif int(value) in range(0,90):
        roll = (512 + (value*3.4))
    else:
        print("Bug"+str(value))
    return int(roll)

def Y_axis(value):
    value = float(value)
    yaw = 512
    if value < -90:
        yaw = 205
    elif int(value) in range(-90, 0):
        yaw = int(512+(value * -6.8))
    elif int(value) in range(0, 90):
        yaw = int(512-(value * 6.8))
    elif value > 90:
        yaw = 819
    else:
        print("Bug"+str(value))
    return int(yaw)

def X_axis(value): #512 964
    value = float(value)
    pitch = 820
    if value < -45:
        pitch = 205
    elif int(value) in range(-45,0):
        pitch = int((value * 6.8) + 820)
    elif int(value) in range(0,45):
        pitch = int((value * 3.4) + 820)
    elif value > 45:
        pitch = 964
    else:
        print("Bug" + str(value))
    return int(pitch)

def qtoe(x,y,z,w):
    #eular YZX
    R11 = 1-(2*((y*y)+(z*z)))
    R21 = 2*((x*y)+(z*w))
    R31 = 2*((x*z)-(w*y))
    R22 = 1-(2*((x*x)+(w*w)))
    R23 = 2*((y*z)-(w*x))
    C2 = sqrt((R11*R11)+(R31*R31))
    thata_1 = degrees(atan2((R31/-C2),(R11/C2)))
    thata_2 = degrees(atan2((R21),(-C2)))
    thata_3 = degrees(atan2((R23/-C2),(R22/-C2)))
    thata = [thata_1,thata_2,thata_3]
    return thata

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("/operator/head/rotation")
def on_message(client, userdata,msg):
    data_Q = msg.payload.decode("utf-8", "strict")
    data_Q = str(data_Q).split(",")
    eular = (qtoe(float(data_Q[0]),float(data_Q[1]),float(data_Q[2]),float(data_Q[3])))
    Y = eular[0]
    Z = eular[1]+180
    X = eular[2]

    print("Y  " + str(Y) + "  " + str(Y_axis(Y)))
    print("Z  " + str(Z) + "  " + str(Z_axis(Z)))
    print("X  " + str(X) + "  " + str(X_axis(X)))

    DynamixelgoalposID2 = X_axis(X)
    DynamixelgoalposID3 =  Z_axis(Z)
    DynamixelgoalposID12 = Y_axis(Y)

    m(3, DynamixelgoalposID3)
    m(2, DynamixelgoalposID2)
    m(12, DynamixelgoalposID12)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_forever()



