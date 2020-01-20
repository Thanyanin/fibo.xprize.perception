import paho.mqtt.client as mqtt
from dynamixel_control import Dynamixel
from math import atan2,sqrt,degrees
# X,Y,Z หมายถึงการหมุนรอบแกน

host = "192.168.2.102" 
port = 1883

portDynamixel = Dynamixel('COM6',1000000) #comport,barudrate
portDynamixel.connect()
motor_type = "Ax" #ชนิดของ Motor

def set_Dynamixel(ID, position):
    portDynamixel.setDeviceMoving(ID, motor_type, position, 1023, 1023)#ID, type, goal position, goal speed, max torque

def position_known(ID):
    return portDynamixel.getMotorPosition(ID)


def Z_axis(value):
    value = float(value)
    roll = 512
    if int(value) in range(270,360) or int(value) in range(0,90):
        if int(value) in range(270,360):
            roll = (512 + ((value-360) * 3.4))
        elif int(value) in range(0,90):
            roll = (512 + (value*3.4))
    return int(roll)

def Y_axis(value):
    value = float(value)
    yaw = 512
    if int(value) in range(-90,90):
        if int(value) in range(-90, 0):
            yaw = int(512+(value * -3.4))
        elif int(value) in range(0, 90):
            yaw = int(512-(value * 3.4))
    return int(yaw)

def X_axis(value):
    value = float(value)
    pitch = 820
    if int(value) in range(-45,45):
        if int(value) in range(-45,0):
            pitch = int((value * 6.8) + 820)
        elif int(value) in range(0,45):
            pitch = int((value * 3.2) + 820)
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
    global pos_ID2_Past, pos_ID3_Past, pos_ID12_Past, pos_ID2_Now, pos_ID3_Now, pos_ID12_Now
    data_Q = msg.payload.decode("utf-8", "strict")
    data_Q = str(data_Q).split(",")
    eular = qtoe(float(data_Q[0]),float(data_Q[1]),float(data_Q[2]),float(data_Q[3]))
    Y = eular[0]
    Z = eular[1]+180
    X = eular[2]

    print("Y  " + str(Y) + "  " + str(Y_axis(Y)))
    print("Z  " + str(Z) + "  " + str(Z_axis(Z)))
    print("X  " + str(X) + "  " + str(X_axis(X)))

    pos_ID2_Now  = X_axis(X)
    pos_ID3_Now  = Z_axis(Z)
    pos_ID12_Now = Y_axis(Y)

    if abs(pos_ID2_Past - pos_ID2_Now) < 100:
            pos_ID2_Past = pos_ID2_Now
    if abs(pos_ID3_Past - pos_ID3_Now) < 100:
            pos_ID3_Past = pos_ID3_Now
    if abs(pos_ID12_Past - pos_ID12_Now) < 100:
            pos_ID12_Past = pos_ID12_Now

    set_Dynamixel(3,  pos_ID2_Past)
    set_Dynamixel(2,  pos_ID3_Past)
    set_Dynamixel(12, pos_ID12_Past)

if __name__ == "__main__":
    DynamixelposID2 = position_known(2)
    DynamixelposID3 = position_known(3)
    DynamixelposID12 = position_known(12)
    DynamixelgoalposID2 = position_known(2)
    DynamixelgoalposID3 = position_known(3)
    DynamixelgoalposID12 = position_known(12)
    
    #X
    pos_ID2_Past  = 850 
    pos_ID2_Now   = 850
    #Z
    pos_ID3_Past  = 512 
    pos_ID2_Now   = 512
    #Y
    pos_ID12_Past = 512 
    pos_ID12_Now  = 512

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host)
    client.loop_forever()



