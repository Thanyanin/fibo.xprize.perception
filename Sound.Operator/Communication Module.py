import socket
import pyaudio


####Client setting
serverAddressPort = ("192.168.2.111", 20000)
bufferSize = 4096
bindPort = ("192.168.2.106", 20001)

####Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100


p = pyaudio.PyAudio()


streamsend = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

streamrecieve = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate= RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)



###Socket Setting###
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockrecieve = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockrecieve.bind(bindPort)

###Connecting...###
print("Connected")

###Streaming####
while True:
    ###Sending Data###
    datasend = streamsend.read(CHUNK)
    sock.sendto(datasend, serverAddressPort)


    ###Recieve Data###
    msgFromServer, addr = sockrecieve.recvfrom(bufferSize)
    streamrecieve.write(msgFromServer, CHUNK)


