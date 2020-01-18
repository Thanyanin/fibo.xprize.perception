#!/usr/bin/python3

import time
import cv2
import math, numpy as np
import socket
import sys, os

SOCKET_HOST = "localhost"
SOCKET_PORT = 1150
SOCKET_BUFF = 1024  # modify in initialization

_FONT_HUD_  = cv2.FONT_HERSHEY_SIMPLEX

print(sys.argv)
if len(sys.argv) >= 2:
    SOCKET_HOST = str(sys.argv[1])

print("[START] in {}".format(os.getcwd()))

print("Initialize socket ...")
sock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setblocking(False)
sock.settimeout(0.01)
bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
SOCKET_BUFF = round(bufsize / 2)
print("Socket sending buffer size = ", bufsize)
print("My sending buffer size = ", SOCKET_BUFF)
print("Sending to {} on port {} ...".format(SOCKET_HOST, SOCKET_PORT))

# START
sock.sendto(str.encode("[START]"), (SOCKET_HOST, SOCKET_PORT))

#region Stream Data
cap = cv2.VideoCapture("./src/video.mp4")

try:

    t_begin = 0
    t_end   = 0
    t_fps   = 0

    counter_error   = 0

    streaming_size  = (round(1920 * 1), round(1080 * 1))

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
                cap = cv2.VideoCapture("./src/video.mp4")
                continue

        counter_error   = 0

        _IMG_HEIGHT_, _IMG_WIDTH_ = frame.shape[:2]

        # Convert
        # img_proc    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_proc    = frame
        img_proc = cv2.resize(img_proc, streaming_size, interpolation=cv2.INTER_NEAREST)
        # Encode
        img_encode  = cv2.imencode(".jpg", img_proc)[1]

        # Stream
        DATA_HEADER = "[HEADER]"
        sock.sendto(str.encode(DATA_HEADER), (SOCKET_HOST, SOCKET_PORT))
        num = len(img_encode)
        num = math.ceil(num / SOCKET_BUFF)

        #region Debug/Decode
        data_stream = b""
        #endregion

        for x in range(num):
            i_begin = x * SOCKET_BUFF
            i_end   = i_begin + SOCKET_BUFF
            sock.sendto(img_encode[i_begin:i_end], (SOCKET_HOST, SOCKET_PORT))

            #region Debug/Decode
            data_stream +=  img_encode[i_begin:i_end].tostring()
            #endregion

        #region Debug/Decode
        img_encode_recv = np.frombuffer(data_stream, np.uint8)
        img_decode      = cv2.imdecode(img_encode_recv, cv2.IMREAD_COLOR)
        #endregion

        # Draw
        tmp_text    = str(round(t_fps))
        textsize    = cv2.getTextSize(tmp_text, _FONT_HUD_, 1, 1)[0]
        cv2.putText(img_proc, tmp_text, (1, 1 + textsize[1]), _FONT_HUD_, 1, (255, 0, 0), 1, cv2.LINE_AA)

        # Display
        # cv2.imshow("src", frame)
        cv2.imshow("img_proc", img_proc)
        cv2.imshow("img_decode (sender)", img_decode)
        # cv2.imshow("img_proc_resize", img_proc_resize)

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