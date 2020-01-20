# Vision Operator
# การส่ง video
ใช้ socket tcp ในการส่งภาพโดยจะ encode เป็น jpeg tcp://192.168.2.101:8888 port ในอนาคตอาจจะเปลี่ยน
# การแปลงภาพเข้าตาซ้ายและขวา
สร้างจอภาพที่มีความยาวที่เหมาะสมมา map กับกล้องของตาซ้ายและกล้องของตาขวาและส่งภาพไปแสดงผลที่ Head Set
# การควบคุมส่วนหัว Avatar
นำค่า rotation ที่ได้จาก Head Set และ rotation จาก Body Tracker มาคำนวณหา rotation ของส่วนหัวที่อ้างอิงกับลำตัว 
จากนั้นส่งค่า rotation ซึ่งเป็นข้อมูล quarternion q0 = x, q1 = y, q2 = z, q3 = w เป็นข้อมูล float 5 ตำแหน่ง
โดยใช้ protocol เป็น mqtt

	Topic: /operator/head/rotation
	Port: 1883
	Format: q0:float,q1:float,q2:float,q3:float

# Mobility
นำค่า rotation ที่ได้จาก Body Tracker มาคำนวณหา rotation เมื่อปรับตำแหน่งอ้างอิงกับ set home เรียบร้อยแล้ว
จากนั้นส่งค่า rotation ซึ่งเป็นข้อมูล quarternion q0 = x, q1 = y, q2 = z, q3 = w เป็นข้อมูล float 5 ตำแหน่ง
โดยใช้ protocol เป็น mqtt

	Topic: /operator/body/rotation
	Port: 1883
	Format: q0:float,q1:float,q2:float,q3:float

# Manipulation
นำค่า rotation ที่ได้จาก Body Tracker , translation และ rotation ของ Left sholder Tracker, Right sholder Tracker มาคำนวณหา rotation และ translation ของตำแหน่งหัวไหล่ที่อ้างอิงกับลำตัว
นำค่า translation และ rotation ที่ได้จาก Left Hand Tracker , translation และ rotation ของ Right Hand Trackerมาคำนวณหา rotation และ translation, rotation ของตำแหน่งมือที่อ้างอิงกับหัวไหล่
จากนั้นส่งค่า rotation ซึ่งเป็นข้อมูล quarternion q0 = x, q1 = y, q2 = z, q3 = w และ translation ในรูปแบบ x,y,z เป็นข้อมูล float 5 ตำแหน่ง
โดยใช้ protocol เป็น mqtt

	Topic: /operator/sholderleft/rotation
	Port: 1883
	Format: q0:float,q1:float,q2:float,q3:float

	Topic: /operator/sholderright/translation
	Port: 1883
	Format: x:float,y:float,z:float

	Topic: /operator/handleft/rotation
	Port: 1883
	Format: q0:float,q1:float,q2:float,q3:float

	Topic: /operator/handright/translation
	Port: 1883
	Format: x:float,y:float,z:float