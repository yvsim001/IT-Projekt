#Import the required Libraries
#import time
import paho.mqtt.client as mqtt
#from dash import Dash, html, Input, Output, dcc
#
from tkinter import *
from tkinter import messagebox
#import PIL
from PIL import Image,ImageTk
from multiprocessing import Process

msg_temperatur=None
msg_humidity=None
 

topics = ['fhdo/itp/gp1/12','fhdo/itp/gp1/11','fhdo/itp/gp1/13']
def on_message(client , userdata, message):
    msg=str(message.payload.decode())
    print(message.topic, '--->', msg)
    if message.topic==topics[0]:
        if msg=="ANALOG":
            Nachricht="Die manuelle Steuerung ist aus!..."
            Fact.set(Nachricht)
        elif msg=="op":
            Fact.set("Welcome....")
        elif msg=="wait":
            Fact.set("Waiting on Movement....")
    if message.topic==topics[1]:
            msg_temperatur="Temperature: "+msg+" °C"
            Fact_temp.set(msg_temperatur)
    if message.topic==topics[2]:
            msg_humidity='Humidity: '+msg+" %"
            Fact_humid.set(msg_humidity)
                    
def on_connect (client, userdata, flags, rc):
            
    client.subscribe ('fhdo/itp/gp1/#')
                
client = mqtt.Client()
BROKER_ADDRESS="broker.emqx.io"


client.on_connect = on_connect
client.on_message =on_message

client. connect (BROKER_ADDRESS)
client. loop_start()
        

        
def btn_on_click():
    client.publish(topics[0], 'open')
    Nachricht ="Der Tür ist geöffnet!..."
    Fact.set(Nachricht)
    
def btn_off_click():
    client.publish(topics[0], 'off')
    Nachricht ="Der Lufter ist aus!..."
    Fact.set(Nachricht)
    
def btn_turn_click():
    client.publish(topics[0], 'turn')
    Nachricht ="Der Lufter ist ein!..."
    Fact.set(Nachricht)
def btn_closed_click():
    client.publish(topics[0], 'closed')
    Nachricht ="Der Tür ist zu!..."
    Fact.set(Nachricht)
               
def btn_press_click():
    messagebox.askquestion("Manuelle Steurerung", "Wollen Sie wirklich die manuelle Steuerung aktivieren?")
    if 'yes':
        client.publish(topics[0], 'press')
        Nachricht="Manuelle Steuerung aktiviert!..."
        Fact.set(Nachricht)
        print(Nachricht)   
    else:
        Nachricht="Die Steuerung ist noch Digital!..."
        Fact.set(Nachricht)
        print(Nachricht)

#Create an instance of tkinter frame
win = Tk()
win.title("IT-Projekt Gruppe1")
        #win.iconbitmap('E:\a.ico')
# Ändert der size des Fenster
win.geometry("1280x620")
# Create text widget and specify size.
titel= Label(win, text="KÜHLRAUM",fg="deep sky blue", bg="royal blue", font="Helvetica 16 bold italic").grid(row=0, column=2, columnspan=2)
Tür=Label(win, text='Tür-Button', fg='black', bg='white', font='verdana').grid(row=3, column=0, columnspan=2)
lufter=Label(win, text='Lufter-Button', fg='black', bg='white', font='verdana').grid(row=3, column=6, columnspan=2)
       
        
global Fact
global Fact_temp
global Fact_humid

Fact=StringVar()
Fact_temp=StringVar()
Fact_humid=StringVar()

Fact.set("--Stand--")
Fact_temp.set('--Temperature--')
Fact_humid.set('--Humidity--')

my_img	= ImageTk.PhotoImage(Image.open("fh.png"))
Bild= Label(image=my_img).grid(row=2, column=2,rowspan=8)

temperatur_info= Label(win, textvariable=Fact_temp, fg="black", bg="white", font="VERDANA").grid(row=6,column=0,columnspan=2)
feutchtigkeit_info= Label(win, textvariable=Fact_humid, fg="black", bg="white", font="VERDANA").grid(row=6,column=6,columnspan=2)
stand= Label(win, textvariable=Fact, fg="black", bg="white", font="VERDANA").grid(row=10,column=2,columnspan=3)


bouton0=Button(win, text="OPEN", relief=RAISED,fg="SpringGreen4",bg="SpringGreen2", font="VERDANA",padx=30, command= btn_on_click).grid(row=4,column=0)
bouton1=Button(win, text="Turn_ON", relief=RAISED, fg="blue4",bg="turquoise1", font="VERDANA",padx=30, command=btn_turn_click ).grid(row=4, column=6)
bouton2=Button(win, text="CLOSED", relief=RAISED, fg="white",bg="grey28", font="VERDANA",padx=30, command=btn_closed_click ).grid(row=4,column=1)
bouton3=Button(win, text="Turn_OFF", relief=RAISED, fg="white",bg="grey28", font="VERDANA",padx=30, command=btn_off_click).grid(row=4, column=7) 
bouton4=Button(win, text="Schließen", relief=SUNKEN, cursor="spider",fg="white",bg="red2", font="IMPACT",command=win.quit).grid(row=10,column=7)
bouton5=Button(win, text="MANUELLE", relief=GROOVE, cursor="spider",fg="DarkOrange1",bg="WHITE", font="IMPACT",command=btn_press_click).grid(row=10,column=0)

win.mainloop()


   

