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

#Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
bufferSize = 4096

#Server setting
Server_IP = str(sys.argv[1])
Server_Port = 20000

#Device setting
print(SoundDeviceDetector())
Input = int(input("Type 'Mic' Index : "))
Output = int(input("Type 'Sound Output' Index : "))

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((Server_IP, Server_Port))

#Stream Setting
pa = p.open(format=p.get_format_from_width(WIDTH),
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=False,
            frames_per_buffer=CHUNK,
            input_device_index=Input,
            output_device_index=Output)


print("* streaming")

connected_IP = []
while True:
    try:
        # Receive
        data_IN, address = sock.recvfrom(bufferSize)  # buffer size is 4096 bytes
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

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

    except Exception:
        print("Exception", sys.exc_info())
        break



