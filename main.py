import network, time, urequests
from machine import Pin
from utime import sleep, sleep_ms
from dht import DHT22
from umqtt.simple import MQTTClient
import ujson


sensor1 = DHT22(Pin(12)) 
sensor2 = DHT22(Pin(14))

MQTT_CLIENT_ID = "will1234unico"
MQTT_BROKER = "test.mosquitto.org"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = "will/publica"

SSID = "ANGGIE PAU"
PASSWORD = "Molly2049"



def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():             
          miRed.active(True)                   
          miRed.connect(red, password)         
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():        
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

if conectaWifi (SSID, PASSWORD):
    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())

    print("Conectando a  MQTT server... ",MQTT_BROKER,"...", end="")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect() 
    
while True:
    try:
        sensor1.measure()
        temp1 = sensor1.temperature()
        #hum1 = sensor1.humidity()
        sensor2.measure()
        temp2 = sensor2.temperature()
        #hum2 = sensor2.humidity()
        print('Temperatura uno: ',temp1,' °C ','Temperatura dos: ',temp2,' °C' )
        message = ujson.dumps({"temperatura_uno":temp1, "temperatura_dos":temp2 })
        
        print("Reportando a  MQTT topic {}: {}".format(MQTT_TOPIC, message))
        
        client.publish(MQTT_TOPIC, message)
        
    except OSError as e:
        print('Failed to read sensor.', e)
    time.sleep(2)