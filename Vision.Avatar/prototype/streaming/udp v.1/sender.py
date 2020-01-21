#!/usr/bin/python3

import time
import cv2
import math, numpy as np
import socket
import sys, os
import zlib

SOCKET_HOST = "localhost"
SOCKET_PORT = 1150
SOCKET_BUFF_SIZE = 32768

_FONT_HUD_  = cv2.FONT_HERSHEY_SIMPLEX

print(sys.argv)
if len(sys.argv) >= 2:
    SOCKET_HOST = str(sys.argv[1])

print("[START] in {}".format(os.getcwd()))

print("Initialize socket ...")
sock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setblocking(False)
sock.settimeout(3)
bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print("Socket sending buffer size = ", bufsize)
bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print("Socket receiving buffer size = ", bufsize)

print("My sending buffer size = ", SOCKET_BUFF_SIZE)
print("Sending to {} on port {} ...".format(SOCKET_HOST, SOCKET_PORT))

# START
sock.sendto(str.encode("[START]"), (SOCKET_HOST, SOCKET_PORT))

#region Stream Data
cap = cv2.VideoCapture("../src/video.mp4")

try:

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    counter_error   = 0

    streaming_size  = (round(1920 * 0.5), round(1080 * 0.5))

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
        img_proc    = frame
        img_proc = cv2.resize(img_proc, streaming_size, interpolation=cv2.INTER_NEAREST)
        # Encode
        # img_send_raw    = img_proc.ravel() # convert to raw (1d)
        img_send_encode = cv2.imencode(".jpg", img_proc)[1] # convert to jpg
        # img_send_gzip   = zlib.compress(img_send_raw) # convert to gzip

        # Stream
        DATA_HEADER = "[HEADER]"
        sock.sendto(str.encode(DATA_HEADER), (SOCKET_HOST, SOCKET_PORT))
        # num = len(img_send_raw)   # data size : raw
        num = len(img_send_encode)   # data size : encode
        # num = len(img_send_gzip)   # data size : gzip
        print("Send {} byte".format(num))
        num = math.ceil(num / SOCKET_BUFF_SIZE)

        #region Debug/Decode
        data_stream = b""
        #endregion

        for x in range(num):
            i_begin = x * SOCKET_BUFF_SIZE
            i_end   = i_begin + SOCKET_BUFF_SIZE
            # sock.sendto(img_send_raw[i_begin:i_end], (SOCKET_HOST, SOCKET_PORT))  # send data : raw
            sock.sendto(img_send_encode[i_begin:i_end], (SOCKET_HOST, SOCKET_PORT))  # send data : encode
            # sock.sendto(img_send_gzip[i_begin:i_end], (SOCKET_HOST, SOCKET_PORT))  # send data : gzip

            #region Debug/Decode
            # data_stream +=  img_send_raw[i_begin:i_end].tostring()    # receive simulation : raw
            data_stream +=  img_send_encode[i_begin:i_end].tostring()    # receive simulation : encode
            # data_stream +=  img_send_gzip[i_begin:i_end]    # receive simulation : gzip
            #endregion

        #region Debug/Decode
        img_recv_raw        = np.frombuffer(data_stream, np.uint8)              
        # img_recv_raw_cvt    = img_recv_raw.reshape(streaming_size[1], streaming_size[0], 3) # final data simulation : raw
        img_recv_decode     = cv2.imdecode(img_recv_raw, cv2.IMREAD_COLOR)   # final data simulation : encode
        # img_recv_gzip       = zlib.decompress(img_recv_raw)   # final data simulation : gzip
        # img_recv_gzip       = img_recv_gzip.reshape(streaming_size[1], streaming_size[0], 3)
        #endregion

        # Draw
        tmp_text    = str(round(t_fps))
        textsize    = cv2.getTextSize(tmp_text, _FONT_HUD_, 1, 1)[0]
        cv2.putText(img_proc, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)

        # Display
        # cv2.imshow("src", frame)
        cv2.imshow("img_proc", img_proc)
        # cv2.imshow("img_recv_raw_cvt (sender)", img_recv_raw_cvt)
        cv2.imshow("img_recv_decode (sender)", img_recv_decode)

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
sock.sendto(str.encode("[END]"), (SOCKET_HOST, SOCKET_PORT))
sock.close()

print("[END]")