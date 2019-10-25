import socket
import pyaudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100


p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)  #Sendto

stream2 = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate= RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK) #Recieve

UDP_IPRecieve = "10.18.251.107"
UDP_PORTRecieve = 5005

UDP_IPsend = "10.18.251.107"
UDP_PORTsend = 5005

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP

sockrecieve = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP

sockrecieve.bind((UDP_IPRecieve, UDP_PORTRecieve))


print("* recording")


while True:
    data2 = stream.read(CHUNK)#sendto
    sock.sendto(data2, (UDP_IPsend, UDP_PORTsend))#sendto
    print(data2)

    data, addr = sockrecieve.recvfrom(10000) # buffer size is 1024 bytes
    stream2.write(data,CHUNK) #recieve
    print(data)

