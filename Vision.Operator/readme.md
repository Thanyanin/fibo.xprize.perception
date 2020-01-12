# Vision Operator

# Maintainer
- [Dew Passakorn](https://www.facebook.com/dew.passakorn21)
- [Ming Ptsy](https://www.facebook.com/ming.ptsy.1)
- [Yanawut Rumdech](https://www.facebook.com/profile.php?id=100002889512694)
- [Ping Nopporn](https://www.facebook.com/nopporn.bussabavalai)
Scene rendering in operator perspective (Virtual World) 

 

การติดตั้งเพื่อใช้งานHTC Vive Pro ร่วมกับSteam

![Capture](https://user-images.githubusercontent.com/56964016/71962235-9bf92380-322b-11ea-8a7f-59088d135218.PNG)

ในการพัฒนาร่วมกับHTC Vive pro ซึ่งประกอบไปด้วยVR Headset, Controllers, Base stations และ Trackers ทำการดาวน์โหลดโปรแกรมSteam และติดตั้งSteamVR พร้อมทั้งตั้งค่าระบบHTC Vive Pro

การติดตั้งเพื่อใช้งานHTC Vive Pro ร่วมกับUnity  

สร้าง3D-Unity project แล้วทำการดาวน์โหลดและImport SteamVR Plugin จากAsset store เพื่อเชื่อมต่อHTC Vive pro system เข้ากับUnity  

![Capture1](https://user-images.githubusercontent.com/56964016/71962354-d4006680-322b-11ea-8f82-0e920bbe4ccb.PNG) 


การใช้งานSteamVR Plugin  

ทำการลากCameraRig จากPrefabs ของSteamVR Plugin เข้ามาในTab Hierarchy โดยCameraRig หนึ่งในPrefabs ที่มากับSteamVR Plugin เป็นPlayer’s area หรือพื้นที่สำหรับการเล่นอ้างอิงจากBase station ที่ถูกติดตั้งของผู้เล่น เพื่อเรียกใช้งาน Right Controller, Left Controller และCamera ของHTC Vive Pro 

![Capture2](https://user-images.githubusercontent.com/56964016/71962393-e8dcfa00-322b-11ea-9cc8-b51cd3817cdc.PNG)
 

การแสดงผลและการมองเห็นของกล้องตาซ้ายและตาขวาของVR Headset  

จากSteam VR Asset ใน[Camera Rig] ซึ่งประกอบไปด้วยController ฝั่งขวากับซ้ายและ Camera(Both eyes) ทำการDuplicate Camera เป็นสองอันและเปลี่ยนการตั้งค่ามุมมองของกล้องจากแบบBoth eyes เป็นLeft eye และRight eye 

จากนั้นสร้าง Quad สำหรับRender วิดีโอRaw data ของกล้องสองตาจากฝั่งAvatar ที่Stream ด้วย ffmpeg และส่งข้อมูลผ่านmqtt มาที่Unity บนmaterial ของQuad ทั้งสอง โดยQuad ทั้งสองจะอยู่แยกกันใน Camera(Left) และ Camera(Right) อย่างละเพลน 

 ![Capture3](https://user-images.githubusercontent.com/56964016/71962568-4f621800-322c-11ea-95b4-4298a7422a7f.PNG)



การทำScene Rendering บนQuad 

![Capture4](https://user-images.githubusercontent.com/56964016/71962606-60ab2480-322c-11ea-902e-ae47524703c5.PNG)


Raw data ถูกส่งเข้ามาที่Unity จากmqtt ซึ่งอยู่ในรูปแบบของวิดีโอ จึงทำการCreate Material เพื่อแปลงRaw Videoเป็นVideo Texture เพื่อนำไปRender บนQuad ทั้งสองและ ให้ขนาดของQuad เท่ากับขนาดของวิดีโอที่ได้จากกล้องสองตา 

![Capture5](https://user-images.githubusercontent.com/56964016/71962629-6c96e680-322c-11ea-9383-6f7430a9a978.PNG)
 
โดยภาพที่ได้จากกล้องสองตาจะมีขนาด 2560x960 px โดยที่แบ่งออกเป็นกล้องจากตาซ้ายและตาขวาอย่างละครึ่งหนึ่ง โดยกล้องทั้งสองมีระยะห่างกัน42 mm และภาพที่ได้มีความละเอียด 2560x960 px และเป็นแบบMirror  

สร้างLayer สำหรับทำCulling mask โดยการกำหนดให้Quad_right เป็นLayer: right_view และQuad_left เป็นLayer: left_view และกำหนดให้ตำแหน่งของQuad ทั้งสองถูกShift เข้ามาหากันให้ซ้อนทับกันเป็นระยะครึ่งหนึ่งของQuad ทั้งนี้เพื่อจะนำไปทำCulling mask ให้ภาพที่มองเห็นผ่านVR Headset ในRight Camera เห็นเพียงภาพจากกล้องฝั่งขวาของกล้องสองตา และLeft Camera เห็นเพียงภาพจากกล้องฝั่งซ้ายจากกล้องสองตาเท่านั้น 

![Capture6](https://user-images.githubusercontent.com/56964016/71962669-8801f180-322c-11ea-9cdd-9e1102a9e710.PNG)


การตั้งค่าและการปรับค่ามุมมองของกล้อง 

ให้กล้องทั้งสองมีProjection แบบPerspective โดยมีการกำหนดตำแหน่ง และระยะระหว่างกล้องดังนี้ 

![Capture7](https://user-images.githubusercontent.com/56964016/71962696-98b26780-322c-11ea-8a1f-beab500d8820.PNG) 

![Capture8](https://user-images.githubusercontent.com/56964016/71962726-ad8efb00-322c-11ea-9e09-6a5da26ac939.PNG)


Culling mask ใช้สำหรับเลือกObject ที่จะแสดงของกล้องโดยการSet layer ของObject นั้น ๆ เพื่อเลือกแสดง โดยในระบบ กล้องตาซ้ายหรือCamera_left จะเลือกแสดงเพียงภาพที่ได้จากกล้องตาซ้ายและกล้องตาขวาหรือCamera_right จะเลือกแสดงเพียงภาพที่ได้จากกล้องตาขวา ดังนั้นจึงตั้งค่าให้Culling mask ของกล้องตาซ้ายแสดงเฉพาะLayer ของleft_view และให้กล้องตาขวาแสดงเฉพาะLayer ของright_view โดยตำแหน่งของQuad ทั้งสองจะอยู่ด้านหน้าCamera หรืออยู่ในField of view ของHeadset camera ทั้งสอง 

![Capture9](https://user-images.githubusercontent.com/56964016/71962745-bc75ad80-322c-11ea-9a74-9d22a1b970e3.PNG)

การตั้งค่าตำแหน่งของQuadและ Headset camera 

การกำหนดตำแหน่งของCamera ทั้งสองเพื่อให้อยู่ในระยะที่เหมาะสมกับภาพจากกล้องตาซ้ายของleft_view และภาพจากกล้องตาขวาของright_view  

 Camera_left 

![Capture10](https://user-images.githubusercontent.com/56964016/71962770-cbf4f680-322c-11ea-9435-9aeb2b5ab27c.PNG)
 
Camera_right 

![Capture11](https://user-images.githubusercontent.com/56964016/71962772-cbf4f680-322c-11ea-991f-5cedbdaeac81.PNG)


การกำหนดตำแหน่งของQuad ทั้งสองที่ซ้อนทับกันเพื่อให้กล้องของตาซ้ายแสดงภาพจากกล้องตาซ้ายจากLayer: left_view และให้กล้องของตาขวาแสดงภาพจากกล้องตาขวาจากLayer: right_view  

Quad_left 

![Capture12](https://user-images.githubusercontent.com/56964016/71962774-cc8d8d00-322c-11ea-95c5-b11eaf33f880.PNG)

Quad_right 

![Capture13](https://user-images.githubusercontent.com/56964016/71962776-cd262380-322c-11ea-8529-d0c607be40d6.PNG) 

 

 
