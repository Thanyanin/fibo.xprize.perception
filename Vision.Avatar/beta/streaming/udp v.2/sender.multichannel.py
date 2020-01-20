#!/usr/bin/python3

import time
import cv2
import math, numpy as np
import socket
import sys, os
import zlib
import threading

PRESET_IMG_SIZE = (int(1920 * 1), int(1080 * 1))

SOCKET_HOST = "192.168.1.1"
SOCKET_PORT = 10000 # start port
SOCKET_CH_NUM  = 8
SOCKET_CONN_LIST    = []    # socket connection list
PROTOCOL_DATA_DELIMITER = b"[HEADER]"
SOCKET_BUFF_SIZE = 32768

_FONT_HUD_  = cv2.FONT_HERSHEY_SIMPLEX

print(sys.argv)
if len(sys.argv) >= 2:
    SOCKET_HOST = str(sys.argv[1])

print("[START] in {}".format(os.getcwd()))

for ch in range(SOCKET_CH_NUM):
    print("Initialize socket port {} for ch {} ...".format(SOCKET_PORT + ch, ch))
    SOCKET_CONN_LIST.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    SOCKET_CONN_LIST[ch].settimeout(10)

    # set socket option
    bufsize = SOCKET_CONN_LIST[ch].getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print("Socket sending buffer size = ", bufsize)
    bufsize = SOCKET_CONN_LIST[ch].getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print("Socket receiving buffer size = ", bufsize)

print("My sending buffer size = ", SOCKET_BUFF_SIZE)

# START

#region Stream Data

cap = cv2.VideoCapture("../src/video.mp4")

try:

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    t_display_data  = 0

    counter_error   = 0

    while(cap.isOpened()):

        t_begin = time.perf_counter()

        ret, frame  = cap.read()
        if ret is False or ret is None:
            counter_error   += 1
            # exit
            if counter_error > 30:
                print("Error limited : Read data fail !")
                break
            else:
                print("Restart to frame 0")
                cap = cv2.VideoCapture("../src/video.mp4")
                continue

        counter_error   = 0

        _IMG_HEIGHT_, _IMG_WIDTH_ = frame.shape[:2]

        # Convert
        img_full = cv2.resize(frame, PRESET_IMG_SIZE, interpolation=cv2.INTER_NEAREST)
        _IMG_HEIGHT_, _IMG_WIDTH_ = img_full.shape[:2]
        for ch in range(SOCKET_CH_NUM):

            # Slice/Cut
            img_height_per_ch    = int(_IMG_HEIGHT_ / SOCKET_CH_NUM)
            img_py_start    = int(ch * img_height_per_ch)
            img_slice   = img_full[img_py_start:img_py_start + img_height_per_ch, 0:_IMG_WIDTH_]

            # Encode
            # img_send_raw    = img_slice.ravel() # convert to raw (1d)
            img_send_jpeg = cv2.imencode(".jpg", img_slice)[1] # convert to jpg
            # img_send_gzip   = zlib.compress(img_slice) # convert to gzip

            # num = len(img_send_raw)   # data size : raw
            num = len(img_send_jpeg)   # data size : jpeg
            # num = len(img_send_gzip)   # data size : gzip
            print("Send to {}:{} = {} byte".format(SOCKET_HOST, SOCKET_PORT + ch, num))

            # Stream
            SOCKET_CONN_LIST[ch].sendto(PROTOCOL_DATA_DELIMITER, (SOCKET_HOST, SOCKET_PORT + ch))   # send HEADER
            SOCKET_CONN_LIST[ch].sendto(img_send_jpeg, (SOCKET_HOST, SOCKET_PORT + ch))   # send jpeg
            # SOCKET_CONN_LIST[ch].sendto(img_send_gzip, (SOCKET_HOST, SOCKET_PORT + ch))   # send gzip
            
        # Draw
        tmp_text    = str(round(t_fps))
        textsize    = cv2.getTextSize(tmp_text, _FONT_HUD_, 1, 1)[0]
        cv2.putText(img_full, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)

        # Display
        cv2.imshow("img_full", img_full)

        if cv2.waitKey(1) & 0xff == 27:
            print("Esc is pressed.\nExit")
            break

        t_end   = time.perf_counter()
        t_fps   = 1 / (t_end - t_begin)

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    pass

except Exception:
    print("Exception", sys.exc_info())
    pass

cap.release()
cv2.destroyAllWindows()

#endregion

# END
for ch in range(SOCKET_CH_NUM):
    print("Closing socket ch {}".format(ch))
    SOCKET_CONN_LIST[ch].close()

print("[END]")