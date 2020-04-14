###########################################################
###  Sistema de apoyo en el suministro de Medicamentos  ###
###########################################################
********************************************
***               Autores                ***
********************************************
Andres Felipe Vargas
Felipe Alberto Castro
Diseño con microprosesadores y microcontroladores
Ingeniería Electrónica
Universidad Industrial de Santander - UIS
********************************************
***        Descripción general           ***
********************************************
Lenguaje de programación: Micropython
IDE utilizado: uPyCraft
Board:Esp-32s nodeMCU
Ide App: AppInventor
Interrupciones: WakeUp cause por RTC(Real Time Clock)
Uso de diferentes tipos de memoria: Se usa las memorias flash para guardar los archivos y SRAM para guardar las variables de ejecución del script.

Timers: RTC
Protocolo de comunicación: i2c
********************************************
***    Descripción de los archivos       ***
********************************************
Data.txt -> Datos guardados en la memoria flash de la tarjeta
Dispensador.py -> Archivo con el script principal
esp8266_i2c_lcd.py -> Libreria para usar la LCD mediante protocolo i2c
lcd_api.py -> Libreria que es usada por esp8266_i2c_lcd.py
main.py -> Archivo que se ejecuta por defecto (este ejecuta al codigo principal Dispensador.py)
mqtt.py -> Libreria para usar el protocolo mqtt
Medic_Pro.aia -> Aplicación diseñada en App inventor.
agregar.php -> Agrega medicamentos a la tabla de usuario.
conex.php -> Realiza la conexión con la base de datos.
crear.php ->  Crea una tabla para cada usuario deonde se almacenan los datos de los medicamentos.
eliminar.php -> Elimina una fila de datos de la tabla de usuario dependiendo el medicamento que se quiera eliminar.
leer.php -> lee la tabla de usuario para imprimir en la pantalla la informacion de los medicamentos.
LeerBase.php -> Script para analizar y comparar base de datos de la ESP32 con la base de datos mysql. 
registrar -> añade una fila a la tabla de usuarios `users` con los datos del nuevo registro.
users.php -> valida la información de usuario y contraseña para el inicio de sesión en la aplicación.
 
