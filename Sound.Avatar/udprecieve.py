import socket
import pyaudio
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
p = pyaudio.PyAudio()

UDP_IP = "192.168.1.191"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)

while True:
    data, addr = sock.recvfrom(10000) # buffer size is 1024 bytes

    stream.write(data,CHUNK)
