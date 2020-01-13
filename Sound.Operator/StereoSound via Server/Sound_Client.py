import socket
import pyaudio
import sys

p = pyaudio.PyAudio()

def SoundDeviceDetector():
    print("Sound Device List:")
    i=0
    while True:
        try:
            print(p. get_device_info_by_index(i))
            i += 1
        except:
            break
    return "-------------------------------------------------"

#Client setting
Server_IP = str(sys.argv[1])
Server_Port = 20000

#Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
bufferSize = 4096

#Device setting
print(SoundDeviceDetector())
Input = int(input("Type 'Mic' Index : "))
Output = int(input("Type 'Sound Output' Index : "))


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#Stream Setting
pa = p.open(format=p.get_format_from_width(WIDTH),
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK,
            input_device_index=Input,
            output_device_index=Output)

serverAddressPort = (Server_IP, Server_Port)

#Streaming
while True:
    try:
        data_OUT = pa.read(CHUNK) #Reading Data
        sock.sendto(data_OUT, serverAddressPort) #Sending Data

        data_IN, address = sock.recvfrom(bufferSize) #Recieve Data
        pa.write(data_IN, CHUNK) #streaming Data
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

    except Exception:
        print("Exception", sys.exc_info())
        break



