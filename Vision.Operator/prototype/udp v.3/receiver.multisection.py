#!/usr/bin/python3

import time
import cv2
import math, numpy as np
import socket
import sys, os
import zlib
import threading

PRESET_IMG_SIZE = (int(2560 * 1), int(960 * 1))
PRESET_IMG_SECTION_NUM  = 16

SOCK_CONN   = None
SOCKET_HOST = "0.0.0.0" # any interface
SOCKET_PORT = 1112
PROTOCOL_DATA_DELIMITER = b"[HEADER]"
SOCKET_BUFF_SIZE = int((PRESET_IMG_SIZE[0] * PRESET_IMG_SIZE[1]) * 3) + len(PROTOCOL_DATA_DELIMITER) + 1

_FONT_HUD_  = cv2.FONT_HERSHEY_SIMPLEX

def MyThreadStreamReader():

    print(">MyThreadStreamReader() => {}".format(threading.current_thread().getName()))

    global SOCK_CONN, SOCKET_PORT
    SOCKET_BUFFER_DATA  = b""

    index_begin = None
    index_end   = None

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    try:

        while True:

            # read data
            data, addr  = SOCK_CONN.recvfrom(SOCKET_BUFF_SIZE)
            SOCKET_BUFFER_DATA  += data

            #region Find HEADER
            while(True):
                if index_begin == None:
                    res = SOCKET_BUFFER_DATA.find(PROTOCOL_DATA_DELIMITER)
                    if res >= 0:
                        # print("Begin index = ", res)
                        index_begin = res
                        index_end   = None
                    else:
                        break
                else:
                    res = SOCKET_BUFFER_DATA.find(PROTOCOL_DATA_DELIMITER, index_begin + len(PROTOCOL_DATA_DELIMITER))
                    if res > index_begin:
                        # print("End index = ", res)
                        index_end   = res

                        try:

                            #region Data Extraction
                            package_number = SOCKET_BUFFER_DATA[index_begin + len(PROTOCOL_DATA_DELIMITER):index_begin + len(PROTOCOL_DATA_DELIMITER) + 1]
                            img_package_num = int.from_bytes(package_number, "big")
                            if img_package_num < 0 or img_package_num >= PRESET_IMG_SECTION_NUM:
                                # Decoding fail
                                print("Skip bad header ({})".format(img_package_num))
                            else:
                                data_extract    = SOCKET_BUFFER_DATA[index_begin + len(PROTOCOL_DATA_DELIMITER) + 1:index_end]
                                # print("Receive (pkg#{}) {} byte".format(img_package_num, len(data_extract)))

                                if len(data_extract) > 0:
                                    img_recv_raw    = np.frombuffer(data_extract, np.uint8)

                                    # print("Decoding ...")
                                    # img_recv_raw_cvt    = img_recv_raw.reshape(PRESET_IMG_SIZE[1], PRESET_IMG_SIZE[0], 3)   # image raw
                                    img_recv_decode     = cv2.imdecode(img_recv_raw, cv2.IMREAD_COLOR)  # image decode

                                    if img_recv_decode is not None:
                                        
                                        # Draw
                                        # print("Performance calculation")
                                        t_end   = time.perf_counter()
                                        t_fps   = 1 / (t_end - t_begin)
                                        t_begin = time.perf_counter()

                                        tmp_text    = str(round(t_fps))
                                        textsize    = cv2.getTextSize(tmp_text, _FONT_HUD_, 1, 1)[0]
                                        # cv2.putText(img_recv_raw_cvt, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)    # image raw
                                        cv2.putText(img_recv_decode, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)  # image decode

                                        # Recontrsuction Data
                                        # print("Reconstruction ...")
                                        img_height_per_pkg  = int(PRESET_IMG_SIZE[1] / PRESET_IMG_SECTION_NUM)
                                        img_py_start        = int(img_package_num * img_height_per_pkg)
                                        IMAGE_RESULT_DATA[img_py_start:img_py_start + img_height_per_pkg, 0:PRESET_IMG_SIZE[0]]  = img_recv_decode

                                    else:
                                        print("Skip decoding section {} fail !".format(img_package_num))

                                else:
                                    print("! Skip empty data in section {}".format(img_package_num))

                            # remove DATA from buffer (shift data to begin position)
                            # print("shift data to begin position")
                            SOCKET_BUFFER_DATA  = SOCKET_BUFFER_DATA[index_end:]

                            # reset index
                            index_begin = index_end = None

                            #endregion

                        except Exception:
                            print("! Data Extraction :", sys.exc_info())
                    else:
                        break


            # Clear Buffer
            if len(SOCKET_BUFFER_DATA) > SOCKET_BUFF_SIZE * 2:
                # clear tmp
                print("Clear buffer ({})!".format(len(SOCKET_BUFFER_DATA)))
                SOCKET_BUFFER_DATA  = b""

            #endregion

    except Exception:
        print("! MyThreadStreamReader() :", sys.exc_info())

    finally:
        print("<MyThreadStreamReader() => {}".format(threading.current_thread().getName()))

#=======================================================================================================================================#

print("[START] in {}".format(os.getcwd()))

print("Initialize socket {}:{} ...".format(SOCKET_HOST, SOCKET_PORT))
SOCK_CONN   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Binding ...")
SOCK_CONN.bind((SOCKET_HOST, SOCKET_PORT))
SOCK_CONN.settimeout(10)

# set socket option
bufsize = SOCK_CONN.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print("Socket sending buffer size = ", bufsize)
bufsize = SOCK_CONN.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print("Socket receiving buffer size = ", bufsize)

print("Waiting for data ...")

try:

    IMAGE_RESULT_DATA   = np.zeros((PRESET_IMG_SIZE[1], PRESET_IMG_SIZE[0], 3), np.uint8)

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    #region Create Stream Reader Thread

    thread  = threading.Thread(target=MyThreadStreamReader, name="My Stream Reader")
    thread.start()

    #endregion

    while True:
        
        try:

            cv2.imshow("IMAGE_RESULT_DATA", IMAGE_RESULT_DATA)           # image decode

            if cv2.waitKey(1) & 0xff == 27:
                print("Esc is pressed.\nExit")

                print("Closing socket ...")
                SOCK_CONN.close()

                break

        except Exception:
            print("Exception : ", sys.exc_info())

except KeyboardInterrupt:
    print("KeyboardInterrupt")

except Exception:
    print("Exception", sys.exc_info())

print("[END]")