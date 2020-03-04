# FIBO XPRIZE : Perception Unit
ออกแบบและพัฒนาระบบเกี่ยวกับ Sense ทั้ง 5 ของมนุษย์ ประกอบไปด้วย `Sight`, `Hearing`, Smell, Taste, และ Touch  การออกแบบและพัฒนาระบบของ Perception Unit จะมุ่งเน้น 2 เรื่องคือ Sight และ Hearing


# สารบัญ
- [ภาพรวมของระบบ](#ภาพรวมของระบบ)
- [การเชื่อมต่อกับอุปกรณ์ต่าง ๆ](#การเชื่อมต่อกับอุปกรณ์ต่าง-ๆ)
- [Feature](#feature-freeeeeeze-)
- [ทีม](#ทีม)
- [รูปแบบการทำงาน](#รูปแบบการทำงาน)
- [Network Configuration](#network-configuration)
- [Communication](#communication)


# ภาพรวมของระบบ
![System Overview](src/img/Perception&#32;System&#32;Overview&#32;-&#32;2019-10-23&#32;C.png)


# การเชื่อมต่อกับอุปกรณ์ต่าง ๆ
![ยังไม่มีรูป](src/img/Peripheral&#32;-&#32;2020-02-06&#32;A.png)
รายละเอียดของแต่ละส่วนสามารถอ่านได้ในหัวข้อ [Feature (*freeeeeeze !*)](#feature-freeeeeeze-)


# Feature (*freeeeeeze !*)
- การส่ง-รับภาพจาก Avatar ไปยัง Operator ([รับภาพ](Vision.Operator), [ส่งภาพ](Vision.Avatar/beta/streaming))
- การควบคุมมุมมองของ Avatar จาก Operator ([ส่ง Pose ของ Operator](Vision.Operator), [ควบคุมหัวของ Avatar](Vision.Avatar))
- การสื่อสารด้วยเสียงระหว่าง Operator ผ่าน Avatar กับ Recipient ([Operator](Sound.Operator), [Avatar](Sound.Avatar))


# ทีม
- [SLAM](SLAM)
- [3D Sound](3D Sound)
- [Virtual Environment](Virtual Environment)
- [Motion Capture](Motion Capture)


# รูปแบบการทำงาน
## Direct Mode (กำลังพัฒนา)
![Direct Mode](src/img/Perception&#32;-&#32;Direct&#32;Mode&#32;-&#32;2019-12-12&#32;A.png)
การทำงานของระบบแบบเรียบง่ายและไม่ซับซ่อน  การเคลื่อนไหวของ Operator ในการปรับเปลี่ยนมุมมองจะถูกส่งตรงไปยัง Avatar จากนั้นข้อมูล**ภาพ**และ**เสียง**จะถูกถ่ายทอดสดส่งตรงจาก Avatar กลับมายัง Operator โดยไม่มีการปรุงแต่งข้อมูลใด ๆ ทั้งสิ้น
*เมื่อระบบเกิด Delay จะทำให้การเคลื่อนไหวของ Operator และ Avatar ไม่สอดคล้องกัน*

## Virtual Reality Mode (กำลังพัฒนา)
![Virtual Reality Mode](src/img/Perception&#32;-&#32;Virtual&#32;Reality&#32;Mode&#32;-&#32;2019-12-12&#32;B.png)
การทำงานของระบบแบบโลกเสมือน  การเคลื่อนไหวของ Operator ในการปรับเปลี่ยนมุมมองจะถูกไปยัง Virtual World ในขณะที่ Avatar จะทำการเก็บข้อมูลต่าง ๆ เช่น ภาพ เสียง แรงดัน และอุณหภูมิ เป็นต้น ส่งไปยัง Virtual World เช่นเดียวกัน  ภายใน Virtual World จะรวบรวมข้อมูลต่าง ๆ เพื่อสร้างสภาพแวดล้อมที่สอดคล้องกับข้อมูลจาก Avatar เช่น ข้อมูล**ภาพ**และ**เสียง**อาจถูกปรับปรุง/สังเคราะห์ขึ้นมาใหม่ เป็นต้น  Operator จะเสมือนตัวละครที่เข้าไปอยู่ใน Virtual World ดังกล่าวและสามารถเคลื่อนที่ไปยังจุดต่าง ๆ หรือปฏิสัมพันธ์กับ Virtual World ได้ ในขณะที่ Avatar ก็จะทำการเคลื่อนที่และปฏิสัมพันธ์กับ Real World ซึ่งสอดคล้องกับ Virtual World ด้วยเช่นกัน
*Virtual World จะตอบสนองอย่างรวดเร็วต่อ Operator เพื่อหลอกเสมือนไม่มี Delay เกิดขึ้นในระบบ*


# Network Configuration
![ยังไม่มีรูป](http://www.google.com/search?q=ยังไม่มีรูป+private+network.jpg)
- Broker ([Mosquitto](https://www.mosquitto.org)) จะติดตั้งอยู่ที่ Avatar โดยใช้ MQTT Protocol ในการสื่อสารระหว่าง Operator และ Avatar


# Communication
การสื่อสารระหว่าง Application ทั้งหมดจะใช้ MQTT Protocol

## Operator
- *(การทดลอง)* แสดงค่า Rotation ของ Operator ใน Topic ชื่อว่า `/operator/rotation` เพื่อใช้ในการควบคุม**การหมุนหัว**ของ Avatar  ~~รูปแบบของข้อมูลคือ `<roll>,<pitch>,<yaw>`~~ **(ในอนาคตจะเปลี่ยนไปใช้ Quaternion)**

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
