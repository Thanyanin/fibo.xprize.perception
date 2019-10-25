import socket
import pyaudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()
UDP_IP = "192.168.1.159"

UDP_PORT = 5005

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    data = stream.read(CHUNK)
    sock.sendto(data, (UDP_IP, UDP_PORT))



