#!/usr/bin/python3

# Connect to server then receive Image data stream

import time
import cv2
import math, numpy as np
import socket
import sys, os

PROTOCOL_DATA_DELIMITER = b"[HEADER]"
PRESET_IMG_SIZE = (int(1920 * 1), int(1080 * 1))
PRESET_IMG_FORMAT   = "BGR"
PRESET_IMG_CH   = len(PRESET_IMG_FORMAT)

SOCKET_HOST = "localhost"
SOCKET_PORT = 1150
SOCKET_BUFF_SIZE = (PRESET_IMG_SIZE[0] * PRESET_IMG_SIZE[1] * PRESET_IMG_CH) + len(PROTOCOL_DATA_DELIMITER)

_FONT_HUD_  = cv2.FONT_HERSHEY_SIMPLEX

print("[START] in {}".format(os.getcwd()))

print("Initialize socket ...")
sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print("Socket receiving buffer size = ", bufsize)

try:

    SOCKET_BUFFER_DATA  = b""
    SOCKET_DATA = None

    index_begin = None
    index_end   = None

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    counter_error   = 0

    print("Connecting ...")
    sock.connect((SOCKET_HOST, SOCKET_PORT))
    print("Connected")
    print("Request format")
    sock.sendall(PRESET_IMG_FORMAT.encode("ascii"))

    while True:
        
        try:
            
            data    = sock.recv(SOCKET_BUFF_SIZE)
            SOCKET_BUFFER_DATA  += data

            #region Tune HEADER

            if index_begin == None:
                res = SOCKET_BUFFER_DATA.find(PROTOCOL_DATA_DELIMITER, 0)
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

                    data_extract    = SOCKET_BUFFER_DATA[index_begin + len(PROTOCOL_DATA_DELIMITER):index_end]
                    print("Extract data {} byte".format(len(data_extract)))
                    img_encode_recv = np.frombuffer(data_extract, np.uint8)
                    # img_decode      = cv2.imdecode(img_encode_recv, cv2.IMREAD_COLOR)
                    img_decode  = img_encode_recv.reshape(PRESET_IMG_SIZE[1], PRESET_IMG_SIZE[0], PRESET_IMG_CH)

                    # Draw
                    t_end   = time.perf_counter()
                    t_fps   = 1 / (t_end - t_begin)
                    t_begin = time.perf_counter()
                    print("t_fps={}".format(t_fps))

                    tmp_text    = str(round(t_fps))
                    textsize    = cv2.getTextSize(tmp_text, _FONT_HUD_, 1, 1)[0]
                    cv2.putText(img_decode, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)

                    # Display
                    cv2.imshow("img_decode", img_decode)

                    # remove DATA from buffer
                    print("buffer size before shifting = {}".format(len(SOCKET_BUFFER_DATA)))
                    SOCKET_BUFFER_DATA  = SOCKET_BUFFER_DATA[index_end:]
                    print("buffer size after shifting = {}".format(len(SOCKET_BUFFER_DATA)))

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

        if len(SOCKET_BUFFER_DATA) > SOCKET_BUFF_SIZE * 5:
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