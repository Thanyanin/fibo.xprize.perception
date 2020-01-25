# udp v.3
โปรแกรมต้นแบบการ Streaming ส่งข้อมูลภาพจาก Avatar ไปยัง Operator ด้วยอุปกรณ์ Webcam หรือไฟล์ Video  ใช้ Opencv และ Python 3 ในการพัฒนา

# การใช้งาน
~~~
python sender.multisection.py <param1> <param2>
~~~

## Parameter
### param1
device index (0, 1, 2, ...) ที่ต้องการใช้ในการอ่านข้อมูลภาพเพื่อใช้ในการ Streaming

### param2
IP Address ของเครื่องเป้าหมาย (รับข้อูล) ในการการ Streaming

## ตัวอย่างการส่งข้อมูลจากไฟล์ Video (../src/video.mp4) ไปยัง localhost
~~~
python sender.multisection.py
~~~

## ตัวอย่างการส่งข้อมูลจาก Webcam ตัวที่ 0 ไปยังเครื่องคอมพิวเตอร์ที่มี IP Address = กกก.ขขข.คคค.งงง
~~~
python sender.multisection.py 0 กกก.ขขข.คคค.งงง
~~~

# Note

- Convert Image (numpy) to string/ string to Image (numpy)
  - https://stackoverflow.com/questions/17967320/python-opencv-convert-image-to-byte-string/25592959

- Maximum package size over the network
  - https://www.reddit.com/r/learnpython/comments/3nxxws/sockets_how_large_should_a_message_sent_on_a/

- Steaming protocol comparison
  - https://www.wowza.com/blog/streaming-protocols

- Background Subtraction
  - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html  