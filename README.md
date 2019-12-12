# FIBO XPRIZE : Perception Unit
ออกแบบและพัฒนาระบบเกี่ยวกับ Sense ทั้ง 5 ของมนุษย์ ประกอบไปด้วย `Sight`, `Hearing`, Smell, Taste, และ Touch  การออกแบบและพัฒนาระบบของ Perception Unit จะมุ่งเน้น 2 เรื่องคือ Sight และ Hearing


# System Overview
![System Overview](src/img/Perception&#32;System&#32;Overview&#32;-&#32;2019-10-23&#32;C.png)
ภาพรวมของระบบ


# Feature (*freeeeeeze !*)
- การรับภาพจาก Avatar (Stereoscopic) ([Link 1](Vision.Operator), [Link 2](Vision.Avatar))
- การควบคุมมุมมองของ Avatar ([Link 1](Vision.Operator), [Link 2](Vision.Avatar))
- การสื่อสารด้วยเสียง ([Link 1](Sound.Operator), [Link 2](Sound.Avatar))


# Mode
![Direct Mode](src/img/Perception&#32;Mode&#32;-&#32;2019-09-26&#32;B.png)
รูปแบบการทำงานสำหรับ Direct Mode
![Virtual Reality Mode](src/img/Perception&#32;Mode&#32;-&#32;2019-09-26&#32;B.png)
รูปแบบการทำงานสำหรับ Virtual Reality Mode


# Network Configuration
![รูป](http://www.google.com/search?q=รูป private network)
- Broker ([Mosquitto](www.mosquitto.org)) จะติดตั้งอยู่ที่ Avatar โดยใช้ MQTT Protocol ในการสื่อสารระหว่าง Operator และ Avatar


# Communication
## Operator
- *(การทดลอง)* แสดงค่า Rotation ของ Operator ใน Topic ชื่อว่า `/operator/rotation` เพื่อใช้ในการควบคุม**การหมุนหัว**ของ Avatar  รูปแบบของข้อมูลคือ `<roll>,<pitch>,<yaw>` **(ในอนาคตจะเปลี่ยนไปใช้ Quaternion)**
    - **roll**
      - ค่า**บวก**แสดงถึงการเอียงคอไปทางขวา มีค่ามากกว่า `0.0` ถึง `+90.0` มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
      - ค่า**ศูนย์** แสดงถึงการเอียงคอตรง มีค่าเท่ากับ `0.0`  มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
      - ค่า**ลบ**แสดงถึงการเอียงคอไปทางซ้าย มีค่าน้อยกว่า `0.0` ถึง `-90.0` มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
    - **pitch**
      - ค่า**บวก**แสดงถึงการเงิยหน้าขึ้น มีค่ามากกว่า `0.0` ถึง `+90.0` มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
      - ค่า**ศูนย์** แสดงถึงการมองตรง มีค่าเท่ากับ `0.0`  มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
      - ค่า**ลบ**แสดงถึงการก้มหน้าลง มีค่าน้อยกว่า `0.0` ถึง `-90.0` มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
    - **yaw**
      - ค่า**บวก**แสดงถึงการหันไปทางขวา มีค่ามากกว่า `0.0` ถึง `+90.0` มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
      - ค่า**ศูนย์** แสดงถึงการมองตรง มีค่าเท่ากับ `0.0`  มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
      - ค่า**ลบ**แสดงถึงการหันไปทางซ้าย มีค่าน้อยกว่า `0.0` ถึง `-90.0` มีหน่วยเป็น **Degree** ข้อมูลประเภท **Floting**
- *(การทดลอง, หน้าที่หลักของทีม mobility)* แสดงคำสั่งการบังคับของ Operator ใน Topic ชื่อว่า `/operator/remote` เพื่อใช้ควบคุม**ความเร็วและทิศทาง**ในการเคลื่อนที่ของ Avatar  รูปแบของข้อมูลคือ `<throttle>,<steering>`
  - **throttle**
    - ค่า**บวก**แสดงถึงการเดินหน้า มีค่ามากกว่า `0.0` ถึง `1.0` ข้อมูลประเภท **Floting**
    - ค่า**ศูนย์** แสดงถึงการหยุดอยู่กับที่ มีค่าเท่ากับ `0.0` ข้อมูลประเภท **Floting**
    - ค่า**ลบ**แสดงถึงการถอยหลัง มีค่าน้อยกว่า `0.0` ถึง `-1.0` ข้อมูลประเภท **Floting**
  - **steering**
    - ค่า**บวก**แสดงถึงการเลี้ยว/หมุนขวา มีค่ามากกว่า `0.0` ถึง `1.0` ข้อมูลประเภท **Floting**
    - ค่า**ศูนย์** แสดงถึงการหยุดเลี้ยว/หมุน มีค่าเท่ากับ `0.0` ข้อมูลประเภท **Floting**
    - ค่า**ลบ**แสดงถึงการเลี้ยว/หมุนซ้าย มีค่าน้อยกว่า `0.0` ถึง `-1.0` ข้อมูลประเภท **Floting**

## Avatar
- *(การทดลอง)* แสดงค่าระยะห่างที่ตรวจวัดได้ระหว่าง Avatar และ Obstacle ด้านหน้า ใน Topic ชื่อว่า `/avatar/distance` เพื่อใช้ในการแสดงข้อมูลให้แก่ Operator  รูปแบบของข้อมูลคือ `<distance>`
  - **distance**
    - ค่า**บวก**แสดงถึงระยะทางที่วัดได้ มีค่าระหว่าง `0.0` ถึง `100.0` มีหน่วยเป็น **Meter** ข้อมูลประเภท **Floting**
    - ค่า**ลบ**แปลว่าไม่สามารถวัดระยะทางได้ มีค่า**น้อยกว่า** `0.0` มีหน่วยเป็น **Meter** ข้อมูลประเภท **Floting**

# Note
- ให้แต่ละทีมย่อยทำการ **Commit** ไปยัง **Branch** ของทีมตัวเอง
- เมื่อพัฒนาหรือแก้ใขเสร็จแล้ว ให้ทำการ **Pull Request** กลับเข้ามาที่ **Master Branch**
- เก็บ Source Code ต่าง ๆ ไว้ตาม Directory ของทีมย่อยตัวเอง ประกอบไปด้วย [Vision.Operator](Vision.Operator), [Vision.Avatar](Vision.Avatar), [Sound.Operator](Sound.Operator), และ [Sound.Avatar](Sound.Avatar)
