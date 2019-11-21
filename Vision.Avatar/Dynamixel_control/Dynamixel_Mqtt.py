import paho.mqtt.client as mqtt
# from dynamixel_control import Dynamixel
from squaternion import euler2quat, quat2euler, Quaternion

# host = "192.168.1.246"
# port = 1883
host = "broker.mqttdashboard.com"
port = 8000
# portDynamixel = Dynamixel('COM6',1000000)
# portDynamixel.connect()
# motor_type = 'Ax'


# def m(ID, position):
#     portDynamixel.setDeviceMoving(ID, motor_type, position, 1023, 1023)#ID, type, goal position, goal speed, max torque
# def p(ID):
#     return portDynamixel.getMotorPosition(ID)

# DynamixelposID3 = p(3)
# DynamixelposID2 = p(2)
# DynamixelposID12 = p(12)
# DynamixelgoalposID3 = p(3)
# DynamixelgoalposID2 = p(2)
# DynamixelgoalposID12 = p(12)

def X_axis(value):
    value = float(value)
    roll = 512
    if value < -90:
        roll = 2
    elif value > 0 or value < 0 or value == 0:
        roll = int((value * 5.6) + 512)
    elif value > 90:
        roll = 1022
    else:
        print("Bug"+str(value))
    return roll

def Y_axis(value):
    value = float(value)
    yaw = 512
    if value < -90:
        yaw = 2
    elif value > 0 or value < 0 or value == 0:
        yaw = int((value*5.6)+512)
    elif value > 90:
        yaw = 1022
    else:
        print("Bug"+str(value))
    return yaw

def Z_axis(value):
    value = float(value)
    pitch = 820
    if value < -90:
        pitch = 500
    elif value > 0:
        pitch = int((value*2.2)+820)
    elif value == 0:
        pitch = int(820)
    elif value < 0:
        pitch = int(820+(value*3.5))
    elif value > 90:
        pitch = 1020

    return pitch


def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    # self.subscribe("/operator/rotation")
    self.subscribe("TEST/MQTT")
def on_message(client, userdata,msg):
    data_Q = msg.payload.decode("utf-8", "strict")
    print(data_Q)
    if "," in data_Q:
        data_Q = str(data_Q).split(",")
        print(data_Q)
        data = quat2euler(float(data_Q[0]),float(data_Q[1]),float(data_Q[2]),float(data_Q[3]),degrees=True)
        print(data)
        if len(data) == 3:
            # DynamixelgoalposID3 = X_axis(data[0])
            # DynamixelgoalposID2 = Z_axis(data[1])
            # DynamixelgoalposID12 = Y_axis(data[2])
            # m(3, DynamixelgoalposID3)
            # m(2, DynamixelgoalposID2)
            # m(12, DynamixelgoalposID12)
            print([X_axis(data[0]),Z_axis(data[1]),Y_axis(data[2])])
            
        else:
            print("WTF " + str(data))
    else:
        print("WTF " + str(data))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_forever()



