import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep

import dht11

import re
import luma  #bibliothek luma, luma.led_matrix müssen installiert werden 
from luma.led_matrix.device import max7219 
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

led =[29,31,33,35,38] # Pin led
interrupt=22 #Button_pin für Break
b= 12   #Buzzer Pin
relay_pin = 40   #relay Pin
motion_pin = 16  #Den Pin des Bewegungssensors einer Variable zuweisen.
servoPin = 37  #Servo Pin

GPIO.setmode(GPIO.BOARD) #Die GPIO Boardkonfiguration benutzen.
GPIO.setwarnings(False)

GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.setup(interrupt, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Hier wird den Pin als Input gesezt.
GPIO.setup(motion_pin, GPIO.IN)  #Der Pin der Deklarierten Variable wird als Input gesetzt.
GPIO.setup(servoPin, GPIO.OUT)   # Set servoPin to OUTPUT mode


#------------------------------------------------------------------------------------------------------------------
def tür():
    GPIO.setup(servoPin, GPIO.OUT)
    servo1 = GPIO.PWM(servoPin,50) # pin 37 for servo1 frequenz 50Hz
    servo1.start(0)
    # Turn servo1 to 90
    servo1.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    # Wait for 2 seconds
    time.sleep(3)
    
    # servo1 back to 0
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    servo1.stop()
    #GPIO.cleanup()

#------------------------------------------------------------------------------------------------------------------
def tür_zu():
    GPIO.setup(servoPin, GPIO.OUT)
    servo1 = GPIO.PWM(servoPin,50) # pin 37 for servo1 frequenz 50Hz
    servo1.start(0)
    # servo1 back to 0
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    servo1.stop()
    #GPIO.cleanup()
#-------------------------------------------------------------------------------------------------------------------
def tür_auf():
    GPIO.setup(servoPin, GPIO.OUT)
    servo1 = GPIO.PWM(servoPin,50) # pin 37 for servo1 frequenz 50Hz
    servo1.start(0)
    # Turn servo1 to 90
    servo1.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    servo1.stop()
    #GPIO.cleanup()

#------------------------------------------------------------------------------------------------------------------

def ledwater():
    for i in led:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i , GPIO.HIGH)
        #led on
        sleep(0.5)
        if i==38:
            break;
    
    #led off
    GPIO.output(led , GPIO.LOW)
 
#------------------------------------------------------------------------------------------------------------------ 
  
def temp():
    # read data using pin 14
    instance = dht11.DHT11(7)
    result = instance.read()

    while not result.is_valid():  # read until valid values
        result = instance.read()
    
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
    return result

#------------------------------------------------------------------------------------------------------------------

def matrix(result):
    # Matrix Gerät festlegen und erstellen.
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded= 1, block_orientation=90,
    rotate= 0)
    # Matrix Initialisierung in der Konsole anzeigen
    print("[-] Matrix initialized")
    matrix0=str(result.temperature)
    matrix2=str(result.humidity)
    client.publish("fhdo/itp/gp1/11",matrix0)
    client.publish("fhdo/itp/gp1/13",matrix2)
    global matrix1
    matrix1=  "Temperature "+matrix0 +"C"
    # Ausgegebenen Text in der Konsole Anzeigen
    print("--Temperature: %s Grad --" % matrix0)
    show_message(device, matrix1 , fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)

#------------------------------------------------------------------------------------------------------------------

def on_open():
    global open_1
    open_1='Door Open.....'
    client.publish("fhdo/itp/gp1/12",'op')
    print(open_1)
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.5)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
    ledwater()
    # Oeffne Relais
    GPIO.output(relay_pin, GPIO.LOW)
    # warte eine halbe Sekunde
    time.sleep(0.5)
    # schliesse Relais
    GPIO.output(relay_pin, GPIO.HIGH)
    # Wird der print Befehl ausgeführt
    time.sleep(0.1)
    # 0,1 Sekunde Warten
    # Beginn einer Schleife
    tür()
#------------------------------------------------------------------------------------------------------------------------------
def Turn_on():
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded= 1, block_orientation=90,
    rotate= 0)
    show_message(device, 'On' , fill="white", font=proportional(CP437_FONT), scroll_delay=0.7)
def Turn_off():
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded= 1, block_orientation=90,
    rotate= 0)
    show_message(device, 'Off' , fill="white", font=proportional(CP437_FONT), scroll_delay=0.8)
#------------------------------------------------------------------------------------------------------------------------------
def on_open_msg():
    global open_1
    open_1='Door Open.....'
    print(open_1)
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.5)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
    ledwater()
    # Oeffne Relais
    GPIO.output(relay_pin, GPIO.LOW)
    # warte eine halbe Sekunde
    time.sleep(0.5)
    # schliesse Relais
    GPIO.output(relay_pin, GPIO.HIGH)
    # Wird der print Befehl ausgeführt
    time.sleep(0.1)
    # 0,1 Sekunde Warten
    # Beginn einer Schleife
    tür_auf()
    

#------------------------------------------------------------------------------------------------------------------

def motion():
   while GPIO.input(interrupt)==GPIO.HIGH :             
        if(GPIO.input(motion_pin) == 1):   # Wenn der Sensor Input = 1 ist
            print ("Bewegung Erkannt!")  # Wird der print Befehl ausgeführt
            on_open()
            result = temp()
            matrix(result)
            time.sleep(0.1)              # 0,1 Sekunde Warten
            #if(GPIO.input(motion_pin) == 0):     # Wenn der Sensor Input = 0 ist
            #print ("Keine Bewegung ...") # Wird der print Befehl ausgeführt
   global a
   
   a="Die analoge Steuerung ist aus!"
   print(a)
   client.publish("fhdo/itp/gp1/12","ANALOG")
   GPIO.cleanup(servoPin)  # der servopin muss nach jeder Drehung gelöscht werden damit es immer die gleiche drehung macht
#------------------------------------------------------------------------------------------------------------------

#Der Analog-Steuerung muss mit dem UP-Bottom ausgeschaltet werden, damit sich die RPi mit dem Broker anschließt
def on_message (client, userdata, message):
        msg = str (message.payload.decode ("utf-8"))
        print(message.topic,'-->' ,msg)
        if message.topic=="fhdo/itp/gp1/12":
            if msg=="open":
                on_open_msg()
                result=temp()
                matrix(result)
            elif msg=='closed':
                tür_zu()
            elif msg=='turn':
                Turn_on()
            elif msg=='off':
                Turn_off()
            elif msg=="press":
                print('Pressed...')
                motion()

#------------------------------------------------------------------------------------------------------------------

def on_connect (client, userdata, flags, rc):
    
        client.subscribe ('fhdo/itp/gp1/#')

#------------------------------------------------------------------------------------------------------------------
        
BROKER_ADDRESS="broker.emqx.io"

client = mqtt.Client ()

client.on_connect = on_connect

client.on_message =on_message

client. connect (BROKER_ADDRESS)


print ("Connected to MQTT Broker:"+" broker.emqx.io")

motion()


client. loop_forever()





