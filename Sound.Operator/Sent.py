import socket
import pyaudio

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
# RECORD_SECONDS = 1024

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

UDP_IP = "192.168.1.191"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP


print("* recording")


while True:
    data = stream.read(CHUNK)
    sock.sendto(data, (UDP_IP, UDP_PORT))


print("* done")

stream.stop_stream()
stream.close()

p.terminate()

