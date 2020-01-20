import socket
import pyaudio


####Client setting

serverAddressPort   = ("192.168.2.100", 20000)
bufferSize          = 4096
bindPort = ("192.168.1.159",20000)

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
                frames_per_buffer=CHUNK)  #Sendto

streamrecieve = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate= RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK) #Recieve

###Socket Setting###
#Send#
socksend = socket.socket(family=socket.AF_INET, # Internet
                    type= socket.SOCK_DGRAM) # UDP

#Recieve#
sockrecieve = socket.socket(family=socket.AF_INET,# Internet
                    type= socket.SOCK_DGRAM) # UDP
sockrecieve.bind(bindPort)

###Connecting###
print("Connected server!!!")

###Streaming###
while True:
    ###Sending Data###
    datasend = streamsend.read(CHUNK)#sendto
    socksend.sendto(datasend, serverAddressPort)

    ###Recieve Data###
    msgFromServer , addr = sockrecieve.recvfrom(bufferSize)
    streamrecieve.write(msgFromServer, CHUNK) #recieve


