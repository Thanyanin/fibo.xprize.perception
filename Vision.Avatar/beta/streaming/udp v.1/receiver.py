#!/usr/bin/python3

import time
import cv2
import math, numpy as np
import socket
import sys, os

PRESET_IMG_SIZE = (int(1920 * 0.25), int(1080 * 0.25))

# SOCKET_HOST = "localhost"
SOCKET_HOST = "0.0.0.0" # any interface
SOCKET_PORT = 1150
PROTOCOL_DATA_DELIMITER = b"[HEADER]"
SOCKET_BUFF_SIZE = (PRESET_IMG_SIZE[0] * PRESET_IMG_SIZE[1]) + len(PROTOCOL_DATA_DELIMITER)

_FONT_HUD_  = cv2.FONT_HERSHEY_SIMPLEX

print("[START] in {}".format(os.getcwd()))

print("Initialize socket ...")
sock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Binding ...")
sock.bind((SOCKET_HOST, SOCKET_PORT))
# sock.setblocking(False)
sock.settimeout(3)
bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print("Socket sending buffer size = ", bufsize)
bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print("Socket receiving buffer size = ", bufsize)

print("My sending buffer size = ", SOCKET_BUFF_SIZE)
print("Sending to {} on port {} ...".format(SOCKET_HOST, SOCKET_PORT))
print("Waiting for data ...")
try:

    SOCKET_BUFFER_DATA  = b""
    SOCKET_DATA = None

    index_begin = None
    index_end   = None

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    counter_error   = 0

    while True:
        
        try:
            
            data, addr  = sock.recvfrom(SOCKET_BUFF_SIZE)
            SOCKET_BUFFER_DATA  += data

            #region Tune HEADER

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

                    # Display
                    # cv2.imshow("img_recv_raw_cvt", img_recv_raw_cvt)    # image raw
                    cv2.imshow("img_decode", img_recv_decode)           # image decode

                    # remove DATA from buffer
                    SOCKET_BUFFER_DATA  = SOCKET_BUFFER_DATA[index_end:]

                    # reset index
                    index_begin = index_end = None

                    #endregion

            #endregion

            if cv2.waitKey(1) & 0xff == 27:
                print("Esc is pressed.\nExit")
                break

            counter_error   = 0

        except Exception:
            # print("Exception : ", sys.exc_info())
            if counter_error > 100:
                print("Exception : ", sys.exc_info())
                print("Error limit !")
                break
            
            counter_error   += 1
            pass

        if len(SOCKET_BUFFER_DATA) > SOCKET_BUFF_SIZE * 2:
            # clear tmp
            print("Clear buffer ({})!".format(len(SOCKET_BUFFER_DATA)))
            SOCKET_BUFFER_DATA  = b""

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    pass

except Exception:
    print("Exception", sys.exc_info())
    pass

print("[END]")