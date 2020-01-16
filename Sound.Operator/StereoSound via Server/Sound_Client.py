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

#Client setting
Server_IP = str(sys.argv[1])
Server_Port = 20000

#Pyaudio setting
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
bufferSize = 4096
DefaultSettingSwitch = False
Input = 0
Output = 0

#Device setting
if len(sys.argv) == 4:
    Input = int(sys.argv[2])
    Output = int(sys.argv[3])
if (len(sys.argv) == 3) and (sys.argv[2] == 0):
    DefaultSettingSwitch = True
if (len(sys.argv) == 2):
    print(GetInputDeviceInfo())
    Input = int(input("Type 'Mic' Index : "))
    print(GetOutputDeviceInfo())
    Output = int(input("Type 'Sound Output' Index : "))
else:
    raise("Argument Error")

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#Stream Setting
if DefaultSettingSwitch == False:
    pa = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK,
                input_device_index=Input,
                output_device_index=Output)
else:
    pa = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

serverAddressPort = (Server_IP, Server_Port)

print("Connect")
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
print("Disconnect")



