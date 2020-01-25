import socket
import pyaudio

#Client setting
serverAddressPort = ("192.168.1.192", 20000)
bufferSize = 4096

#Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p = pyaudio.PyAudio()
Input = p.open(format=p.get_format_from_width(WIDTH),
               channels=CHANNELS,
               rate=RATE,
               input=True,
               output=False,
               frames_per_buffer=CHUNK)
Output = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)

#Streaming
while True:
    data_OUT = Input.read(CHUNK) #Reading Data
    sock.sendto(data_OUT, serverAddressPort) #Sending Data

    data_IN, addr = sock.recvfrom(bufferSize) #Recieve Data
    Output.write(data_IN, CHUNK) #streaming Data
