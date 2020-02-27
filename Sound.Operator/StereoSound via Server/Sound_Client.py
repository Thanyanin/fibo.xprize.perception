import socket
import pyaudio
import sys
import setting

p = pyaudio.PyAudio()

# Client setting
Server_IP = str(sys.argv[1])
Server_Port = 20000

# Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS_MIC = 1
CHANNELS_SPEAKER = 2
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

serverAddressPort = (Server_IP, Server_Port)

print("Connect")

# Streaming
while True:
    try:
        # Send sound to server
        data_OUT = paMIC.read(CHUNK)  # Reading Data
        sock.sendto(data_OUT, serverAddressPort)  # Sending Data

        # Receive sound from server
        data_IN, address = sock.recvfrom(bufferSize)  # Recieve Data
        paSPEAKER.write(data_IN, CHUNK)  # streaming Data

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

    except Exception:
        print("Exception", sys.exc_info())
        break
print("Disconnect")



