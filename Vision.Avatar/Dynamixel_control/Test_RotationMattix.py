from math import atan2,sqrt,degrees
def qtoe(x,y,z,w):
    #eular YZX
    R11 = 1-(2*((y*y)+(z*z)))
    R21 = 2*((x*y)+(z*w))
    R31 = 2*((x*z)-(w*y))
    R22 = 1-(2*((x*x)+(w*w)))
    R23 = 2*((y*z)-(w*x))
    C2 = sqrt((R11*R11)+(R31*R31))
    # thata_1 = atan2((R31/-C2),(R11/C2))
    # thata_2_C2_plus = atan2((R21),(C2))
    # thata_2_C2_minus = atan2((R21),(-C2))
    # thata_3 = atan2((R23/-C2),(R22/C2))
    # thata=[thata_1,thata_2_C2_minus,thata_2_C2_plus,thata_3]
    thata_1 = degrees(atan2((R31/-C2),(R11/C2)))
    thata_2_C2_plus = degrees(atan2((R21),(C2)))
    thata_2_C2_minus = degrees(atan2((R21),(-C2)))
    thata_3 = degrees(atan2((R23/-C2),(R22/C2)))
    thata=[thata_1,thata_2_C2_minus,thata_2_C2_plus,thata_3]
    return thata

print(qtoe(-0.2878083,-0.002979547,-0.2782989,0.9163554))

