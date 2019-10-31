import socket
import pyaudio
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100

ServerIP='192.168.1.191'
ServerPort=20001

# addr=()

p = pyaudio.PyAudio()
#Send
stream_send = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

sock_send = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

#Recieve
stream_recieve = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate= RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)

sock_recieve = socket.socket(socket.AF_INET, # Internet
                           socket.SOCK_DGRAM) # UDP
sock_recieve.bind((ServerIP, ServerPort))

print("* streaming")
# data_recieve, addr = sock_recieve.recvfrom(4096)
# print('Client IP:'+addr[0])
ip = []
while True:
    #Recieve
    data_recieve, addr = sock_recieve.recvfrom(4096) # buffer size is x bytes
    stream_recieve.write(data_recieve,CHUNK)
    # try:
    #     if addr[0]!=addr2:
    #         print('Client IP:'+addr[0])
    # except:
    #     print('Client IP:'+addr[0])
    try:
        if addr not in ip:
             ip.append(addr)
             print('Connecting...')
             print('Client IP:')
             print(addr)
        # if addr == ():
        #     print('A')

    except:
        pass

    addr2=(addr[0],20001)   #set port to sever's port

    #Send
    data_send = stream_send.read(CHUNK)
    sock_send.sendto(data_send, addr2)


