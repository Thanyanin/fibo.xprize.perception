import socket
import pyaudio
import sys
import setting

p = pyaudio.PyAudio()

# Server setting
Server_IP = str(sys.argv[1])
Server_Port = 20000

# Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS_MIC = 2
CHANNELS_SPEAKER = 1
RATE = 44100
bufferSize = 4096
Input = 0
Output = 0

# Device setting
device = setting.device_setting()
Input = device[0]
Output = device[1]

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((Server_IP, Server_Port))

# Stream Setting

paSPEAKER = p.open(format=p.get_format_from_width(WIDTH),
                   channels=CHANNELS_SPEAKER,
                   rate=RATE,
                   input=False,
                   output=True,
                   frames_per_buffer=CHUNK,
                   output_device_index=Output)

paMIC = p.open(format=p.get_format_from_width(WIDTH),
               channels=CHANNELS_MIC,
               rate=RATE,
               input=True,
               output=False,
               frames_per_buffer=CHUNK,
               input_device_index=Input)


print("* streaming")

connected_IP = []
while True:
    try:
        # Receive sound from client
        data_IN, address = sock.recvfrom(bufferSize)  # buffer size is 4096 bytes
        paSPEAKER.write(data_IN, CHUNK)

        try:
            if address not in connected_IP:
                connected_IP.append(address)
                print('Connecting...')
                print('Client IP:')
                print(address)
        except:
            pass
        # Send sound to client
        data_OUT = paMIC.read(CHUNK)
        sock.sendto(data_OUT, address)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

    except Exception:
        print("Exception", sys.exc_info())

print("* Server Closed")
