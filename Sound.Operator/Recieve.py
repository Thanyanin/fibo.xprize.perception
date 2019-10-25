import socket
import pyaudio

UDP_IP = "192.168.1.159" #ip Guuuu
UDP_PORT = 5005
CHUNK = 1024
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=44100,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)
while True:
    data, addr = sock.recvfrom(10000) # buffer size is 1024 bytes
    stream.write(data,CHUNK)
