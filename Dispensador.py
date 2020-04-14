

import utime as u
import time
import ubinascii
from mqtt import MQTTClient
import machine as m
import network
import socket
import ntptime 
from esp8266_i2c_lcd import I2cLcd

### Globales #####
userId = 1 #User Id
topic_publish='Alarma/medicpro/'+str(userId)
ssid = 'EDWING'
password = '2NB112101584'
DEFAULT_I2C_ADDR = 0x3F
##################
#wifi
#ssid = 'My Asus'
#password = 'felipe98'

#####################################
#####         Funciones         #####
#####################################

#https://github.com/dhylands/python_lcd/tree/master/lcd
def printLCD(text,col,row,opt):
  if (opt=='start'):
    lcd.backlight_on()
    lcd.move_to(col, row)
    lcd.putstr(text)
  else:
    lcd.clear()
    lcd.backlight_off()

#Funcion para encender leds
def ledOnOff(box,on):
  pin=[13,12,14,27,26,25,33,32,35,36,23]
  p=m.Pin(pin[box-1], m.Pin.OUT)
  p.value(on)
  
def readBase():
  data,list=allData()
  data=data.replace('\r','\\r')
  html=http_get('http://self-governing-oppo.000webhostapp.com/LeerBase.php?info='+data+'&User='+str(userId)+'')
  ans=html.split('~+')
  if (ans[0].find('HTTP/1.1 200 OK') != -1):
    if (ans[1]!='noData'):
      dataIn=ans[1]
      dataIn=dataIn.replace('\\r','\r')
      editData(dataIn)
  else:
    readBase()

#funcion para extraer los datos de la mem
def allData():
	f=open('Data.txt','r')
	a=f.read()
	f.close()
	list=a.split('\r')
	for i in range(len(list)):
		list[i]=list[i].split(',')
	return a,list
	
#funcion para mirar las columnas
def someData(list,i):
  y = []
  for row in list:
    if (row[6] != 0):
      y.append(row[i])
  return y

#funcion para grabar nuevos en Data.txt
def editData(newData):
  f=open('Data.txt','w')
  f.write(newData)
  f.close()
  
def takesecond(x):
  return x[1]
#funcion para mirar que medicamento es el siguiente retorna id a deep sleep
def nextId():
  data,list=allData()
  try:
    ntptime.settime()
  except:
    nextId()
  hours=someData(list,2)
  minutes=someData(list,3)
  dateNow=u.localtime()
  dateNow=(dateNow[0],dateNow[1],dateNow[2],dateNow[3]-5,dateNow[4],dateNow[5],dateNow[6],dateNow[7])
  dateNow=u.localtime(u.mktime(dateNow))
  dateMed=[]
  id=[]
  for i in enumerate(hours):
    if (int(hours[i[0]])>=dateNow[3]):
      dateMed.append(u.mktime((dateNow[0],dateNow[1],dateNow[2],int(hours[i[0]]),int(minutes[i[0]]),dateNow[5],dateNow[6],dateNow[7])))
    else:
      dateMed.append(u.mktime((dateNow[0],dateNow[1],dateNow[2]+1,int(hours[i[0]]),int(minutes[i[0]]),dateNow[5],dateNow[6],dateNow[7])))
  for i in enumerate(dateMed):
    timeDiff=dateMed[i[0]]-(u.time()-18000)
    if(timeDiff>0 and timeDiff<3600):
      id.append(i[0])
  if (id==[]):
    print('hora')
    deep_sleep(3600,'0','hora')
  else:
    print('alarma')
    x=[]
    for i in id:
      x.append((i,dateMed[i]))
    x.sort(key=takesecond)
    if (len(x)==1):
      deep_sleep(x[0][1]-u.time()+18000,str(list[x[0][0]][1]),'alarma')
    else:
      strId=str(list[x[0][0]][1])
      i=0
      while True:
        if (i<len(x)-1):
          if (x[i+1][1]-x[i][1]<120):
            strId=strId+'+'+str(list[x[i+1][0]][1])
            i+=1
          else:
            break
        else:
          break
      deep_sleep(x[0][1]-u.time()+18000,strId,'alarma')
      
#funcion sleepmode
def deep_sleep(secs,medi,orden):
  rtc = m.RTC()
  if (orden == 'hora'):
    rtc.memory('hora')
  elif (orden == 'alarma'):
    rtc.memory('alarma,'+medi)
  print('Entrando a deeepsleep')
  m.deepsleep(secs*1000) 

#Funcion para conectar mqtt
def Conexion_MQTT():
    client_id = ubinascii.hexlify(m.unique_id())
    mqtt_server = 'broker.hivemq.com'
    port_mqtt = 1883
    user_mqtt = '' 
    pswd_mqtt = '' 
    client = MQTTClient(client_id, mqtt_server,port_mqtt,user_mqtt,pswd_mqtt) 
    client.set_callback(form_sub)
    client.connect()
    client.subscribe(topic_publish.encode())
    return client
	
#Funcion para reiniciar la coneccion
def Reinciar(a):
  #a=0 para reiniciar normal y a=1 para deeepsleep de 10ms
  if (a==0):
    print('Fallo en la conexion. Intentando de nuevo...')
    time.sleep(10)
    m.reset()
  elif (a==1):
    print('Fallo en la conexion. Intentando de nuevo...')
    time.sleep(10)
    m.deepsleep(10)

#Funcion callback
def form_sub():
  print('')
#funcion para hacer publish	
def do_publish(msg):
  try:
    client = Conexion_MQTT()
  except OSError as e:
    do_publish(msg)
  client.publish(topic_publish.encode(),msg.encode())
  time.sleep(0.1)

#Funcion para obtener HTML ##http://docs.micropython.org/en/latest/esp8266/tutorial/network_tcp.html?highlight=socket
def http_get(url):
  _, _, host, path = url.split('/', 3)
  addr = socket.getaddrinfo(host, 80)[0][-1]
  s = socket.socket()
  s.connect(addr)
  #print(url)
  s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
  while True:
    data = s.recv(1024)
    if data:
      return str(data, 'utf8')
    else:
      break
  s.close()

#####################################
#####            Main           #####
#####################################
i2c = m.I2C(scl=m.Pin(22), sda=m.Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

printLCD('MedicPro UIS',2,0,'start')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False: #Espera a que se conecte a la red
  pass

print('Conexion con el WiFi %s establecida' % ssid)
print(wlan.ifconfig()) #Muestra la IP y otros datos del Wi-Fi
printLCD('',0,0,'end')
data,list=allData()
if (m.reset_cause()==4):
  rtc=m.RTC()
  causa=rtc.memory().decode().split(',')
  print(causa)
  if (causa[0]=='alarma'):
    for i in causa[1].split('+'):
      do_publish(i)
      id=someData(list,1)
      n=id.index(i)
      ledOnOff(int(list[n][5]),1)
      printLCD('Med:',0,0,'start')

      printLCD(list[n][1],4,0,'start')
      printLCD('Cantidad:',0,1,'start')
      printLCD(list[n][4],10,1,'start')
      time.sleep(30)
      ledOnOff(int(list[n][5]),0)
      printLCD('',4,0,'end')
readBase()
data,list=allData()
if (list==['']):
  deep_sleep(3600000,1,'hora')
nextId=nextId()


