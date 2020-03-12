# FIBO XPRIZE : Perception Unit
ออกแบบและพัฒนาระบบเกี่ยวกับ Sense ทั้ง 5 ของมนุษย์ ประกอบไปด้วย `Sight`, `Hearing`, Smell, Taste, และ Touch  การออกแบบและพัฒนาระบบของ Perception Unit จะมุ่งเน้น 2 เรื่องคือ Sight และ Hearing


# สารบัญ
- [ภาพรวมของระบบ](#ภาพรวมของระบบ)
- [การเชื่อมต่อกับอุปกรณ์ต่าง ๆ](#การเชื่อมต่อกับอุปกรณ์ต่าง-ๆ)
- [Function](#function)
- [ทีม](#ทีม)
- [รูปแบบการทำงาน](#รูปแบบการทำงาน)


# ภาพรวมของระบบ
![System Overview](src/img/Perception&#32;System&#32;Overview&#32;-&#32;2019-10-23&#32;C.png)


# การเชื่อมต่อกับอุปกรณ์ต่าง ๆ
![ยังไม่มีรูป](src/img/Peripheral&#32;-&#32;2020-02-06&#32;A.png)


# Function
- Operator สามารถรับรู้ลักษณะทางกายภาพ (ภาพ+เสียง) ในพื้นที่ปฏิบัติการผ่าน Avatar
- Operator ควบคุมการทำงานของ Avatar ด้วยท่าทาง


# ทีม
- [SLAM](SLAM)
- [3D Sound](3D%20Sound)
- [Virtual Environment](Virtual%20Environment)
- [Motion Capture](Motion%20Capture)


# รูปแบบการทำงาน
## Direct Mode (กำลังพัฒนา)
![Direct Mode](src/img/Perception&#32;-&#32;Direct&#32;Mode&#32;-&#32;2019-12-12&#32;A.png)
การทำงานของระบบแบบเรียบง่ายและไม่ซับซ่อน  การเคลื่อนไหวของ Operator ในการปรับเปลี่ยนมุมมองจะถูกส่งตรงไปยัง Avatar จากนั้นข้อมูล**ภาพ**และ**เสียง**จะถูกถ่ายทอดสดส่งตรงจาก Avatar กลับมายัง Operator โดยไม่มีการปรุงแต่งข้อมูลใด ๆ ทั้งสิ้น
*เมื่อระบบเกิด Delay จะทำให้การเคลื่อนไหวของ Operator และ Avatar ไม่สอดคล้องกัน*

## Virtual Reality Mode (กำลังพัฒนา)
![Virtual Reality Mode](src/img/Perception&#32;-&#32;Virtual&#32;Reality&#32;Mode&#32;-&#32;2019-12-12&#32;B.png)
การทำงานของระบบแบบโลกเสมือน  การเคลื่อนไหวของ Operator ในการปรับเปลี่ยนมุมมองจะถูกไปยัง Virtual World ในขณะที่ Avatar จะทำการเก็บข้อมูลต่าง ๆ เช่น ภาพ เสียง แรงดัน และอุณหภูมิ เป็นต้น ส่งไปยัง Virtual World เช่นเดียวกัน  ภายใน Virtual World จะรวบรวมข้อมูลต่าง ๆ เพื่อสร้างสภาพแวดล้อมที่สอดคล้องกับข้อมูลจาก Avatar เช่น ข้อมูล**ภาพ**และ**เสียง**อาจถูกปรับปรุง/สังเคราะห์ขึ้นมาใหม่ เป็นต้น  Operator จะเสมือนตัวละครที่เข้าไปอยู่ใน Virtual World ดังกล่าวและสามารถเคลื่อนที่ไปยังจุดต่าง ๆ หรือปฏิสัมพันธ์กับ Virtual World ได้ ในขณะที่ Avatar ก็จะทำการเคลื่อนที่และปฏิสัมพันธ์กับ Real World ซึ่งสอดคล้องกับ Virtual World ด้วยเช่นกัน
*Virtual World จะตอบสนองอย่างรวดเร็วต่อ Operator เพื่อหลอกเสมือนไม่มี Delay เกิดขึ้นในระบบ*


# Note
- ให้แต่ละทีมย่อยทำการ **Commit** ไปยัง **Branch** ของทีมตัวเอง
- เมื่อพัฒนาหรือแก้ใขเสร็จแล้ว ให้ทำการ **Pull Request** กลับเข้ามาที่ **Master Branch**
- เก็บ Source Code ต่าง ๆ ไว้ตาม Directory ของทีมย่อยตัวเอง ประกอบไปด้วย [Vision.Operator](Vision.Operator), [Vision.Avatar](Vision.Avatar), [Sound.Operator](Sound.Operator), และ [Sound.Avatar](Sound.Avatar)
