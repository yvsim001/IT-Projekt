#Alle definierten Bibliotheken müssen installiert werden
#----------------------------------------------------------------------------------

#Importierung der Bibliothek paho.mqtt.client (mqtt), damit MQTT-clients miteinander kommuniziert
import paho.mqtt.client as mqtt
#Importierung der Bibliothek zum verbinden und steuern von Sensoren und Aktoren
import RPi.GPIO as GPIO
#Importierung der Bibliothek für die Zeit und für den Method sleep()
import time
from time import sleep
#Importierung der Biliothek zur Steuerung des Feutchtigkeitssensors sowie der Temperatur
import dht11
import threading
#bibliothek luma und luma.led_matrix , um einen Text auf einem LED-Matrix-Display anzuzeigen 
import luma   
from luma.led_matrix.device import max7219 
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

#-----------------------------------------------------------------------------------------------
led =[29,31,33,35,38] #Pins led
interrupt=22          #Button_pin für Tkinter
b= 12                 #Buzzer Pin
relay_pin = 40        #relay Pin
motion_pin = 16       #Pin des Bewegungssensors 
servoPin = 37         #Servo Pin
DHT11_pin= 7          #DHT11 Pin
#-----------------------------------------------------------------------------------------
GPIO.setmode(GPIO.BOARD)         #Die GPIO Boardkonfiguration benutzen.
GPIO.setwarnings(False)          #Deaktivieren der Anzeige von GPIO-Warnungen

GPIO.setup(relay_pin, GPIO.OUT)  #konfiguration des Relay_pins als Ausgang
GPIO.setup(led, GPIO.OUT)        #konfiguration der LEDs als Ausgang
GPIO.setup(b, GPIO.OUT)          #Konfiguration des Buzzers als Ausgang
GPIO.setup(servoPin, GPIO.OUT)   # Set servoPin to OUTPUT mode
GPIO.setup(motion_pin, GPIO.IN)  #Der Pin der Deklarierten Variable wird als Input(Eingang) gesetzt.
GPIO.setup(interrupt, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Hier wird den Pin als Eingang gesezt.
#-------------------------------------------------------------------------------------------------------



#--------------Funktion zum automatischen Öffnen und Schließen der Tür -----------------------------------------
def tür():
    GPIO.setup(servoPin, GPIO.OUT)
    # pin 37 for servo1 frequenz 50Hz
    servo1 = GPIO.PWM(servoPin,50)
    # 0° wird für den servo der Referenz position sein
    servo1.start(0)
    # Turn servo1 to 90°
    servo1.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    # Wait for 2 seconds
    time.sleep(3)
    
    # servo1 back to 0°
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    servo1.stop()
    #GPIO.cleanup()

#------------------Funktion nur zum Schließen der Tür-----------------------------------------
def tür_zu():
    GPIO.setup(servoPin, GPIO.OUT)
    # pin 37 for servo1 frequenz 50Hz
    servo1 = GPIO.PWM(servoPin,50)
    # 0° wird für den servo der Referenz position sein
    servo1.start(0)
    # servo1 back to 0°
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    servo1.stop()
    #GPIO.cleanup()
#------------------Funktion nur zum Öffnen der Tür-------------------------------------------------------------------
def tür_auf():
    GPIO.setup(servoPin, GPIO.OUT)
    # pin 37 for servo1 frequenz 50Hz
    servo1 = GPIO.PWM(servoPin,50)
    # 0° wird für den servo der Referenz position sein
    servo1.start(0)
    # Turn servo1 to 90
    servo1.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
    servo1.stop()
    #GPIO.cleanup()

#-----------------------Ankündigung oder Laden der Türöffnung-------------------------------------------------------------

def ledwater():
    for i in led:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i , GPIO.LOW)
        #led on
        sleep(0.5)
        if i==38:
            break;
    #led off
    GPIO.output(led , GPIO.HIGH)
 
#---------------Funktion zum Abrufen der temperature und Feuchtigkeit------------------------------------------------------- 
  
def temp():
    # Temperatur und Feuchtigkeit mit DHT11 abrufen
    instance = dht11.DHT11(DHT11_pin)
    result = instance.read()
    #Ruf Datein bis gültige Werte
    while not result.is_valid():  
        result = instance.read()
    #Anzeigen der Result in der Konsole
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
    return result

#-------------------Funktion zum anzeigen der Temperatur und Feuchtigkeit auf dem Matrix ----------------------------------------------------------------

def matrix(result):
    # Matrix Gerät festlegen und erstellen.
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded= 1, block_orientation=90,rotate= 0)
    # Matrix Initialisierung in der Konsole anzeigen
    print("[-] Matrix initialized")
    #conversion der Abgerufenen Werten im String, damit diese darstellbar seien
    matrix0=str(result.temperature)
    matrix2=str(result.humidity)
    #Die Temperatur und feuchtigkeit wird hier zu der GUI geschickt
    client.publish("fhdo/itp/gp1/11",matrix0)
    client.publish("fhdo/itp/gp1/13",matrix2)
    
    global matrix1
    matrix1=  "Temperature "+matrix0 +"C"
    # Ausgegebenen Text in der Konsole Anzeigen
    print("--Temperature: %s Grad --" % matrix0)
    #Anzeigen der Temperatur 
    show_message(device, matrix1 , fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)

#----------------------Funktion bei der Öffnung der Tür--------------------------------------------------------------------------------------------

def on_open():
    global open_1
    open_1='Door Open.....'
    #veröffebtlichung der Stand der Tür auf der grafischen Benutzeroberfläche
    client.publish("fhdo/itp/gp1/12",'op')
    print(open_1)
    #Buzzer Ton
    #Gebe Geraeusch aus
    GPIO.output(b, GPIO.HIGH)
    #warte eine halbe Sekunde
    time.sleep(0.5)
    #Stoppe Geraeuschausgabe
    GPIO.output(b, GPIO.LOW)
    
    #Led anzeigen
    ledwater()
    
    # Oeffne Relais
    GPIO.output(relay_pin, GPIO.LOW)
    # warte eine halbe Sekunde
    time.sleep(0.5)
    # schliesse Relais
    GPIO.output(relay_pin, GPIO.HIGH)
    # Wird der print Befehl ausgeführt
    time.sleep(0.1)
    # 0,1 Sekunde Warten, dann Öffne der Tür
    tür()
#-----------------------------------------------------------------------------------------------------------------
#--------------------------Ton bei  dem Schließen der Tür mit der GUI---------------------------------------------------------------------------------------
def buzzer_0():
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.25)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
    time.sleep(0.25)
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.5)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
#-------------------------Ton beim Einschalten des Lüfters----------------------------------------------------------------------------------------
def buzzer_1():
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.25)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
    time.sleep(0.25)
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.25)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
#----------------------------------Ton beim Ausschalten des Lüfters--------------------------------------------------------------------------------------------
def buzzer_2():
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.25)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
    time.sleep(0.25)
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.25)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
    time.sleep(0.25)
    #Buzzer Ton
    GPIO.output(b, GPIO.HIGH)
    #Gebe Geraeusch aus
    time.sleep(0.5)
    #warte eine halbe Sekunde
    GPIO.output(b, GPIO.LOW)
    #Stoppe Geraeuschausgabe
#----------------------------------Funktion zur Steurerung des Lüfters--------------------------------------------------------------------------------------------
def Turn_on():
    buzzer_1()
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded= 1, block_orientation=90,
    rotate= 0)
    show_message(device, 'On' , fill="white", font=proportional(CP437_FONT), scroll_delay=0.7)
def Turn_off():
    buzzer_2()
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded= 1, block_orientation=90,
    rotate= 0)
    show_message(device, 'Off' , fill="white", font=proportional(CP437_FONT), scroll_delay=0.8)
#---------------------Funktion beim Öffnen der Tür mit dem GUI ---------------------------------------------------------------------------------------------------------
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
    

#--------------------------------Funktion Zur Nutzung des Bewegungsensors----------------------------------------------------------------------------------
def motion():
        GPIO.setup(interrupt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        client.publish("fhdo/itp/gp1/12",'wait')
        while GPIO.input(interrupt)==GPIO.HIGH :             
            if(GPIO.input(motion_pin) == 1):   # Wenn der Sensor Input = 1 ist
                        print ("Bewegung Erkannt!")  # Wird der print Befehl ausgeführt
                        on_open()                    #Automatisches Öffnen und Schließen der Tür
                        result = temp()
                        matrix(result)                #Darstellung der Temperatur und Feuchtigkeit
                        time.sleep(0.15)              # 0,15 Sekunde Warten
                        client.publish("fhdo/itp/gp1/12",'wait')
                        #if(GPIO.input(motion_pin) == 0):     # Wenn der Sensor Input = 0 ist
                        #print ("Keine Bewegung ...") # Wird der print Befehl ausgeführt
        global a
        a="Die manuelle Steuerung ist aus!"
        print(a)
        #Die Steuerung wird hier nur durch dem GUI gemacht
        client.publish("fhdo/itp/gp1/12","ANALOG")
        GPIO.cleanup(servoPin)# der servopin muss nach jeder Drehung gelöscht werden ,damit er immer die gleiche Drehung macht.
#------------------------  ------------------------------------------------------------------------------------------
#---------------------------Funktion , wenn der Broker mit der vorgegebenen topic eine Nachricht bekommt--------------------------------------------------------
def on_message (client, userdata, message):
        msg = str (message.payload.decode ("utf-8"))
        print(message.topic,'-->' ,msg)
        if message.topic=="fhdo/itp/gp1/12":
            if msg=="open":
                on_open_msg()
                result=temp()
                matrix(result)
            elif msg=='closed':
                buzzer_0()
                tür_zu()
            elif msg=='turn':
                Turn_on()
            elif msg=='off':
                Turn_off()
            elif msg=="press":
                print('Manuelle Steuerung wurde Aktiviert...')
                thread = threading.Thread(target=motion)
                thread.start()

#------------------------------Funktion beim Anschließen oder Abonnement der Client ------------------------------------------------------------------------------------

def on_connect (client, userdata, flags, rc):
    
        client.subscribe ('fhdo/itp/gp1/#')

#----------------------------Anwendung der MQTT- Protokoll--------------------------------------------------------------------------------


BROKER_ADDRESS="broker.emqx.io"

#Objekt der Classe Client wird erstellt
client = mqtt.Client ()
    #subskription der Client
client.on_connect = on_connect

client.on_message =on_message
    #Anschließen mit einem Broker
client. connect (BROKER_ADDRESS)


print ("Connected to MQTT Broker:"+" broker.emqx.io")
#Aufruf der funktion Motion zum automatischen Öffnen und Schließen der Tür
motion()
client.loop_start()



    




