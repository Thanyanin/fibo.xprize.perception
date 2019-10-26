# FIBO XPRIZE Perception Unit
ออกแบบและพัฒนาระบบเกี่ยวกับ Sense ทั้ง 5 ของมนุษย์ ประกอบไปด้วย `Sight`, `Hearing`, Smell, Taste, และ Touch  การออกแบบและพัฒนาระบบจะมุ่งเน้น 2 เรื่องคือ Sight และ Hearing

# System Overview
![System Overview](src/img/Perception&#32;System&#32;Overview&#32;-&#32;2019-10-23&#32;C.png)
ภาพรวมของระบบ

# Operation Mode
![Operation Mode](src/img/Perception&#32;Mode&#32;-&#32;2019-09-26&#32;B.png)
รูปแบบการทำงานสำหรับ Operator

# Communication (MQTT)
## Operator
- แสดงค่า Rotation (roll, pitch, yaw) ของ Operator ใน Topic ชื่อว่า `/operator/rotation`
    - รูปแบบของข้อมูลคือ `<roll>,<pitch>,<yaw>` มีค่าระหว่า `-90.0` ถึง `+90.0` มีหนว่ยเป็น **Degree** ข้อมูลประเภท **Floting**