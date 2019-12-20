import socket
import pyaudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100

Server_IP = '192.168.1.155'
Server_Port = 20000

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((Server_IP, Server_Port))

p = pyaudio.PyAudio()


pa = p.open(format=p.get_format_from_width(WIDTH),
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK)


print("* streaming")

connected_IP = []
while True:
    # Receive
    data_IN, address = sock.recvfrom(4096)  # buffer size is 4096 bytes
    pa.write(data_IN, CHUNK)

    try:
        if address not in connected_IP:
            connected_IP.append(address)
            print('Connecting...')
            print('Client IP:')
            print(address)
    except:
        pass
    # Send
    data_OUT = pa.read(CHUNK)
    sock.sendto(data_OUT, address)
