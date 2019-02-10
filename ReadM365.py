#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bluepy import btle
import os
global vuelta,trama,restantes
trama = ""
vuelta = 0
restantes=""

class MyDelegate(btle.DefaultDelegate):
  def __init__(self):
    btle.DefaultDelegate.__init__(self)

  def handleNotification(self, cHandle, data):
      #print("A notification was received: %s" %data.encode("hex"))
      decodifica(data.encode("hex"))

def decodifica(valor):
  global vuelta, trama,restantes
  tipo = valor[10:12]
  if tipo == "1a":
    print "Firmware version"
    version_software = valor[14:16]+valor[12:14]
    print "Software: "+version_software
  elif tipo == "25":
    print "Km left"
    km_restantes = valor[16:14]+valor[12:14]
    km_restantes = int(km_restantes, 16)
    restantes = km_restantes/10
    print "Km left: "+str(km_restantes/10)
    
  elif tipo == "b0":
    #Ojo, esta es la primera de 3 tramas
   trama = valor
   vuelta = 1
  elif vuelta == 1:
    trama = trama+valor
    vuelta = 2
  elif vuelta ==2:
    os.system('clear')
    vuelta = 0
    trama = trama+valor
    #print "Las tramas son "+trama
    print "Battery :"+str(int(trama[28:30],16))+"%"  
    velocidad = trama[34:36]+trama[32:34]
    velocidad = int(velocidad,16)
    print "Speed: "+str(velocidad/1000)+" Km/h"
    print "Temp: "+str(int(trama[58:60]+trama[56:58],16)/10)+"ºC"  
    print "Km left: "+str(restantes)
  else:
    print "No idea" 
  return 0


print "Connecting..."
p = btle.Peripheral("XX:XX:XX:XX:XX:XX","random")
p.setDelegate(MyDelegate())

p.writeCharacteristic(0x000c, "\x01\x00")


while True:
  if p.waitForNotifications(1.0):
    # handleNotification() was called
    continue

  print("Waiting...")
  #p.writeCharacteristic(0x000e, "\x55\xAA\x03\x20\x01\x1A\x02\xBF\xFF")

  p.writeCharacteristic(0x000e, "\x55\xAA\x03\x20\x01\x25\x02\xB4\xFF")

  p.writeCharacteristic(0x000e, "\x55\xAA\x03\x20\x01\xb0\x20\x0b\xFF")



