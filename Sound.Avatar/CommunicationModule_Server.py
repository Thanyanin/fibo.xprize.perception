import socket
import pyaudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100

Server_IP = '192.168.1.192'
Server_Port = 20000

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((Server_IP, Server_Port))

p = pyaudio.PyAudio()
# Send
Input = p.open(format=p.get_format_from_width(WIDTH),
               channels=CHANNELS,
               rate=RATE,
               input=True,
               output=False,
               frames_per_buffer=CHUNK)

# Receive
Output = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)

print("* streaming")

connected_IP = []
while True:
    # Receive
    data_IN, address = socket.recvfrom(4096)  # buffer size is 4096 bytes
    Output.write(data_IN, CHUNK)

    try:
        if address not in connected_IP:
            connected_IP.append(address)
            print('Connecting...')
            print('Client IP:')
            print(address)


    except:
        pass

    # Send
    data_OUT = Input.read(CHUNK)
    socket.sendto(data_OUT, address)
