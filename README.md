# FIBO XPRIZE Perception Unit
. . .
# System Overview
![System Overview](src/Perception&#32;System&#32;Overview&#32;-&#32;2019-10-23&#32;C.png)
ภาพรวมของระบบ

# Operation Mode
![Operation Mode](src/Perception&#32;Mode&#32;-&#32;2019-09-26&#32;B.png)
รูปแบบการทำงานสำหรับ Operator

# Communication (MQTT Topic)
## Operator
- แสดงค่า Rotation (roll, pitch, yaw) ของ Operator ใน Topic ชื่อว่า `/operator/rotation`
    - รูปแบบของข้อมูลคือ `<roll>,<pitch>,<yaw>` มีค่าระหว่า `-90.0` ถึง `+90.0` มีหนว่ยเป็น **Degree** ข้อมูลประเภท **Floting** 