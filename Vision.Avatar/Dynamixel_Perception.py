import serial
from dynamixel_control import Dynamixel
import cv2
import numpy


# port = Dynamixel('COM10',117647)
port = Dynamixel('COM6',1000000)
port.connect()
motor_type = 'Ax'
# position = motor.getMotorPosition(5)

def m(ID, position):
    port.setDeviceMoving(ID, motor_type, position, 1023, 1023)#ID, type, goal position, goal speed, max torque
def p(ID):
    return port.getMotorPosition(ID)
# robot_head_type = 'Mx'
# port.setDeviceMoving(41, robot_head_type, 2000, 1023, 1023)
# port.setDeviceMoving(42, robot_head_type, 2048, 1023, 1023)

DynamixelposID3 = p(3)
DynamixelposID2 = p(2)
DynamixelposID12 = p(12)
DynamixelgoalposID3 =  p(3)
DynamixelgoalposID2 = p(2)
DynamixelgoalposID12 = p(12)


while(1):
    m(3, DynamixelgoalposID3)
    m(2, DynamixelgoalposID2)
    m(12, DynamixelgoalposID12)
    cv2.imshow("noo",numpy.zeros((100,100)))
    k = cv2.waitKey(1) & 0xFF
        # press 'q' to exit
    if k == ord(' '):
        break
    if k == ord('d'):
        DynamixelgoalposID12 -= 5
    if k == ord('a'):
        DynamixelgoalposID12 += 5
    if k == ord('e'):
        DynamixelgoalposID3 -= 5
    if k == ord('q'):
        DynamixelgoalposID3 += 5
    if k == ord('w'):
        DynamixelgoalposID2 -= 5
    if k == ord('s'):
        DynamixelgoalposID2 += 5
    if k == ord('k'):
        DynamixelgoalposID3 = 500
        DynamixelgoalposID2 = 820
        DynamixelgoalposID12 = 500
