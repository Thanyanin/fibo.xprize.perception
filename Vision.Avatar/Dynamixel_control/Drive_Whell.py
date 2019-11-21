import paho.mqtt.client as mqtt
import serial
host = "192.168.1.246"
port = 1883

ser = serial.Serial('COMXX', 9600, timeout=1)

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    # self.subscribe("/operator/rotation")
    self.subscribe("TEST/MQTT")

def on_message(client, userdata,msg):
    data = msg.payload.decode("utf-8", "strict")
    ser.write(b''+str(data))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_forever()

