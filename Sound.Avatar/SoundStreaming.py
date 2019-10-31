import socket
import pyaudio
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()
#Send
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

UDP_IP_Send = ""
UDP_PORT_Send = 5005

sock_send = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

#Recieve
stream2 = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate= RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)

UDP_IP_Recieve = ""
UDP_PORT_Recieve = 5005

sock_recieve = socket.socket(socket.AF_INET, # Internet
                           socket.SOCK_DGRAM) # UDP
sock_recieve.bind((UDP_IP_Recieve, UDP_PORT_Recieve))

print("* streaming")

while True:
    #Send
    data_send = stream.read(CHUNK)
    sock_send.sendto(data_send, (UDP_IP_Send, UDP_PORT_Send))
    #print(data_send)

    #Recieve
    data_recieve, addr = sock_recieve.recvfrom(10000) # buffer size is x bytes
    stream2.write(data_recieve,CHUNK)
    #print(data_recieve)





