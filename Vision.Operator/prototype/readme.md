# udp v.3
โปรแกรมต้นแบบการ Streaming รับข้อมูลภาพจาก Avatar มายัง Operator  ใช้ Opencv และ Python 3 ในการพัฒนา

# การใช้งาน
~~~
python receiver.multisection.py
~~~

## Parameter
### param1
device index (0, 1, 2, ...) ที่ต้องการใช้ในการอ่านข้อมูลภาพเพื่อใช้ในการ Streaming

### param2
IP Address ของเครื่องเป้าหมาย (รับข้อูล) ในการการ Streaming

# Note

- Convert Image (numpy) to string/ string to Image (numpy)
  - https://stackoverflow.com/questions/17967320/python-opencv-convert-image-to-byte-string/25592959

- Maximum package size over the network
  - https://www.reddit.com/r/learnpython/comments/3nxxws/sockets_how_large_should_a_message_sent_on_a/

- Steaming protocol comparison
  - https://www.wowza.com/blog/streaming-protocols

- Background Subtraction
  - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html  