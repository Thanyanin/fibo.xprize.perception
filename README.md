# FIBO XPRIZE : Perception Unit
ออกแบบและพัฒนาระบบเกี่ยวกับ Sense ทั้ง 5 ของมนุษย์ ประกอบไปด้วย `Sight`, `Hearing`, Smell, Taste, และ Touch  การออกแบบและพัฒนาระบบของ Perception Unit จะมุ่งเน้น 2 เรื่องคือ Sight และ Hearing


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

## Avatar
- แสดงค่าระยะห่างที่ตรวจวัดได้ระหว่าง Avatar และ Obstacle ด้านหน้า *(การทดลอง)*
  - รูปแบบของข้อมูลคือ `<distance>` มีค่าระหว่า `-1.0` ถึง `100.0` มีหนว่ยเป็น **Meter** ข้อมูลประเภท **Floting**
    - **distance**
      - ค่า + แสดงถึงระยะทางที่วัดได้
      - ค่า - แปลว่าไม่สามารถวัดระยะทางได้

# Note
- ให้แต่ละทีมย่อย/คนทำการ **Fork** ไปยัง User ของตัวเอง
- เมื่อพัฒนาหรือแก้ใขเสร็จแล้ว ให้ทำการ **Pull Request** กลับเข้ามาที่ Repo นี้
- เก็บ Source Code ต่าง ๆ ไว้ตาม Directory ของทีมย่อยตัวเอง ประกอบไปด้วย [Vision.Operator](Vision.Operator), [Vision.Avatar](Vision.Avatar), [Sound.Operator](Sound.Operator), และ [Sound.Avatar](Sound.Avatar)