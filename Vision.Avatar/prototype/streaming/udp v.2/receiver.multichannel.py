#!/usr/bin/python3

import time
import cv2
import math, numpy as np
import socket
import sys, os
import zlib
import threading

PRESET_IMG_SIZE = (int(1920 * 1), int(1080 * 1))

SOCKET_HOST = "0.0.0.0" # any interface
SOCKET_PORT = 10000 # start port
SOCKET_CH_NUM  = 8
SOCKET_CONN_LIST    = []    # socket connection list
PROTOCOL_DATA_DELIMITER = b"[HEADER]"
SOCKET_BUFF_SIZE = int((PRESET_IMG_SIZE[0] * PRESET_IMG_SIZE[1]) / SOCKET_CH_NUM) + len(PROTOCOL_DATA_DELIMITER)

_FONT_HUD_  = cv2.FONT_HERSHEY_SIMPLEX

def MyThreadStreamReader(ch):

    print(">MyThreadStreamReader({}) => {}".format(ch, threading.current_thread().getName()))

    global SOCKET_CONN_LIST, SOCKET_PORT
    SOCKET_BUFFER_DATA  = b""

    index_begin = None
    index_end   = None

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    try:

        while True:

            # read data
            data, addr  = SOCKET_CONN_LIST[ch].recvfrom(SOCKET_BUFF_SIZE)
            SOCKET_BUFFER_DATA  += data

            #region Find HEADER

            if index_begin == None:
                res = SOCKET_BUFFER_DATA.find(PROTOCOL_DATA_DELIMITER)
                if res >= 0:
                    # print("Begin index = ", res)
                    index_begin = res
                    index_end   = None
            else:
                res = SOCKET_BUFFER_DATA.find(PROTOCOL_DATA_DELIMITER, index_begin + len(PROTOCOL_DATA_DELIMITER))
                if res > index_begin:
                    # print("End index = ", res)
                    index_end   = res

                    #region extract DATA
                    data_extract        = SOCKET_BUFFER_DATA[index_begin + len(PROTOCOL_DATA_DELIMITER):index_end]
                    img_recv_raw        = np.frombuffer(data_extract, np.uint8)
                    print("Receive {} byte".format(len(data_extract)))

                    #region RAW

                    # if(len(data_extract) != PRESET_IMG_SIZE[0] * PRESET_IMG_SIZE[1] * 3):
                    #     print("Mismatch of data size ({} of {})".format(len(data_extract), PRESET_IMG_SIZE[0] * PRESET_IMG_SIZE[1] * 3))
                    #     continue

                    #endregion

                    # img_recv_raw_cvt    = img_recv_raw.reshape(PRESET_IMG_SIZE[1], PRESET_IMG_SIZE[0], 3)   # image raw
                    img_recv_decode     = cv2.imdecode(img_recv_raw, cv2.IMREAD_COLOR)  # image decode

                    # Draw
                    t_end   = time.perf_counter()
                    t_fps   = 1 / (t_end - t_begin)
                    t_begin = time.perf_counter()

                    tmp_text    = str(round(t_fps))
                    textsize    = cv2.getTextSize(tmp_text, _FONT_HUD_, 1, 1)[0]
                    # cv2.putText(img_recv_raw_cvt, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)    # image raw
                    cv2.putText(img_recv_decode, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)  # image decode

                    # Recontrsuction Data
                    img_height_per_ch    = int(PRESET_IMG_SIZE[1] / SOCKET_CH_NUM)
                    img_py_start    = int(ch * img_height_per_ch)
                    IMAGE_RESULT_DATA[img_py_start:img_py_start + img_height_per_ch, 0:PRESET_IMG_SIZE[0]]  = img_recv_decode

                    # Display
                    # cv2.imshow("img_recv_raw_cvt", img_recv_raw_cvt)    # image raw
                    # cv2.imshow("img ch {}".format(ch), img_recv_decode)           # image decode

                    # remove DATA from buffer
                    SOCKET_BUFFER_DATA  = SOCKET_BUFFER_DATA[index_end:]

                    # reset index
                    index_begin = index_end = None

                    #endregion

            # Clear Buffer
            if len(SOCKET_BUFFER_DATA) > SOCKET_BUFF_SIZE * 2:
                # clear tmp
                print("Clear buffer ({})!".format(len(SOCKET_BUFFER_DATA)))
                SOCKET_BUFFER_DATA  = b""

            #endregion

    except Exception:
        print("! MyThreadStreamReader : ", sys.exc_info())

    finally:
        print("<MyThreadStreamReader({}) => {}".format(ch, threading.current_thread().getName()))

#=======================================================================================================================================#

print("[START] in {}".format(os.getcwd()))

for ch in range(SOCKET_CH_NUM):
    print("Initialize socket port {} for ch {} ...".format(SOCKET_PORT + ch, ch))
    SOCKET_CONN_LIST.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    print("Binding ...")
    SOCKET_CONN_LIST[ch].bind((SOCKET_HOST, SOCKET_PORT + ch))
    SOCKET_CONN_LIST[ch].settimeout(10)
    
    # set socket option
    bufsize = SOCKET_CONN_LIST[ch].getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print("Socket sending buffer size = ", bufsize)
    bufsize = SOCKET_CONN_LIST[ch].getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print("Socket receiving buffer size = ", bufsize)

print("Waiting for data ...")

try:

    IMAGE_RESULT_DATA   = np.zeros((PRESET_IMG_SIZE[1], PRESET_IMG_SIZE[0], 3), np.uint8)

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    #region Create Stream Reader Thread

    for ch in range(SOCKET_CH_NUM):
        thread  = threading.Thread(target=MyThreadStreamReader, name="My Stream Reader {}".format(ch), args=[ch])
        thread.start()

    #endregion

    while True:
        
        try:
            
            cv2.imshow("IMAGE_RESULT_DATA", IMAGE_RESULT_DATA)           # image decode

            if cv2.waitKey(1) & 0xff == 27:
                print("Esc is pressed.\nExit")

                for ch in range(SOCKET_CH_NUM):
                    print("Closing socket ch {} ...".format(ch))
                    SOCKET_CONN_LIST[ch].close()

                break

        except Exception:
            print("Exception : ", sys.exc_info())

except KeyboardInterrupt:
    print("KeyboardInterrupt")

except Exception:
    print("Exception", sys.exc_info())

print("[END]")