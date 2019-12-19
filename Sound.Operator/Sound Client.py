import socket
import pyaudio

#Client setting
serverAddressPort = ("192.168.1.155", 20000)
bufferSize = 4096

#Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p = pyaudio.PyAudio()
pa = p.open(format=p.get_format_from_width(WIDTH),
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK)


#Streaming
while True:
    data_OUT = pa.read(CHUNK) #Reading Data
    sock.sendto(data_OUT, serverAddressPort) #Sending Data

    data_IN, address = sock.recvfrom(bufferSize) #Recieve Data
    pa.write(data_IN, CHUNK) #streaming Data
