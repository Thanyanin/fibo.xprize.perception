import socket
import pyaudio
import sys

p = pyaudio.PyAudio()

def GetInputDeviceInfo():
    print("Input Device: ")
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            n = p.get_device_info_by_host_api_device_index(0, i).get('name')
            print("Input Device id ", i,"-", n.encode("utf8").decode("cp950", "ignore"))
    return "----------------------------------------------------------"

def GetOutputDeviceInfo():
    print("Output Device: ")
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
            n = p.get_device_info_by_host_api_device_index(0, i).get('name')
            print("Output Device id ", i,"-", n.encode("utf8").decode("cp950", "ignore"))
    return "----------------------------------------------------------"

#Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS_MIC = 2
CHANNELS_SPEAKER = 1
RATE = 44100
bufferSize = 4096

Input = 0
Output = 0

#Server setting
Server_IP = str(sys.argv[1])

Server_Port = 20000

#Device setting
if len(sys.argv) == 4:
    Input = int(sys.argv[2])
    Output = int(sys.argv[3])

elif (len(sys.argv) == 3) and (int(sys.argv[2]) == 0):
    Input = None
    Output = None

elif (len(sys.argv) == 2):
    print(GetInputDeviceInfo())
    Input = int(input("Type 'Mic' Index : "))
    print(GetOutputDeviceInfo())
    Output = int(input("Type 'Sound Output' Index : "))
else:
    raise("Argument Error")

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((Server_IP, Server_Port))

#Stream Setting

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
               output=False,
               input=True,
               frames_per_buffer=CHUNK,
               input_device_index=Input)



print("* streaming")

connected_IP = []
while True:
    try:
        # Receive
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
        # Send
        data_OUT = paMIC.read(CHUNK)
        sock.sendto(data_OUT, address)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

    except Exception:
        print("Exception", sys.exc_info())

print("* Server Closed")
