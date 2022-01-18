# -*- coding: utf-8 -*-
"""PoDeS-paginaweb-termal

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eo88W0ULM26lPZmW96Dk8KIA7wf68UnA

Para ejecutar, se debe indicar, python3 podes.py [0,1,2] para iniciar la aplicación, donde 0, 1 ó 2 hace referencia a calidad de las imágenes capturadas, donde 2 es la máxima calidad que permite la cámara.

Ejecutar previamente en el equipo local: 
    pip install wget
    pip install mediapipe
    pip install requests
"""

import os # Librería del sistema operaativo.
import sys
import requests
import xml.etree.ElementTree as ET
import time
import math # Librería matemática.
import threading
import numpy as np # Librería para realizar cálculos númericos.
import wget # Necesita realizar previamente: pip install wget.
import errno
import cv2 # Librería OpenCV para resolver problemas de visualización por ordenador.
import mediapipe as mp # Librería para calcular la pose.
import random
import pandas # Librería utilizada en la creación de la peliculas,
import csv # Librería utilizada en la base de datos. 

#from subprocess import run


# Declaración de las distintas cámaras (ubicación, url, contador de veces detectado movimiento, 
# dirección KNX luminaria y dirección KNX persiana). 
camaras=[['dormitorio','http://192.168.7.222:8891/cgi-bin/CGIProxy.fcgi?usr=admin&pwd=AmgCam18*&cmd=', '/home/ubuntu/pose/', 'diurna/infrarroja', 'ubuntu', '2/1/9'],
         ['cocina','http://192.168.7.223:8892/cgi-bin/CGIProxy.fcgi?usr=admin&pwd=AmgCam18*&cmd=', '/home/ubuntu/pose/', 'diurna/infrarroja', 'ubuntu', '2/1/1'], 
         ['distribuidor','http://192.168.7.224:8893/cgi-bin/CGIProxy.fcgi?usr=admin&pwd=AmgCam18*&cmd=', '/home/ubuntu/pose/', 'diurna/infrarroja', 'ubuntu', '2/1/5'], 
         ['salon','http://192.168.7.225:8894/cgi-bin/CGIProxy.fcgi?usr=admin&pwd=AmgCam18*&cmd=', '/home/ubuntu/pose/', 'diurna/infrarroja', 'ubuntu', '2/3/5'], 
         ['TV','http://192.168.7.226:8895/cgi-bin/CGIProxy.fcgi?usr=admin&pwd=AmgCam18*&cmd=', '/home/ubuntu/pose/', 'diurna/infrarroja', 'ubuntu', '1/2/6'], 
         ['recibidor','http://192.168.7.227:8896/cgi-bin/CGIProxy.fcgi?usr=admin&pwd=AmgCam18*&cmd=', '/home/ubuntu/pose/', 'diurna/infrarroja','ubuntu' , '1/1/9'],
         ['aseo','192.168.7.246', '/home/pi/ImagesGRAYSCALE/foto.jpg', 'térmica', 'pi','raspberry'], # Cámara térmica.
         ['Pepper','192.168.7.14', '/home/nao/recordings/cameras/image.jpg', 'robot', 'nao','nao']] # Cámara del robot Pepper.

ID_camara = 0 # Identificador de la cámara gestionada.
#N_camaras = 1 # Número de cámaras gestionadas.
comando_hacer_fotos='snapPicture2'  # Comando de la cámara para tomar fotos.
comando_habilitar_marca_tiempo='setOSDSetting&isEnableTimeStamp=' # Si ponemos a 1 se muestra la fecha en las capturas, si ponemos a 0 no se muestran
hebras = []

# Configuración del detector de pose
COMPLEJIDAD = 1           #                                                           model_complexity = COMPLEJIDAD
IMAGENES_ESTATICAS = True # STATIC_IMAGE_MODE (true or false). Default to true.       static_image_mode = IMAGENES_ESTATICAS
DETECCION_MINIMA = 0.5    # MIN_DETECTION_CONFIDENCE ([0.0, 1.0]). Default to 0.5.    min_detection_confidence = DETECCION_MINIMA
SEGUIMIENTO_MINIMO = 0.5  # MIN_TRACKING_CONFIDENCE ([0.0, 1.0]). Default to 0.5.     min_tracking_confidence = SEGUIMIENTO_MINIMO
# OTROS PARÁMETROS A PROBAR 
MARCAS_SUAVES = True      # SMOOTH_LANDMARKS (true or false). Default to true.        smooth_landmarks = MARCAS_SUAVES
HABILITAR_SEGMENTACION = False # enable_segmentation = HABILITAR_SEGMENTACION
SUAVIZAR_SEGMENTACION = True # smooth_segmentation=SUAVIZAR_SEGMENTACION

#fotos = np.zeros(N_camaras,dtype=int) # Número de fotografías con pose detectadas.
#foto_con_pose = np.zeros(N_camaras,dtype=int) # Número de fotografías con pose detectadas.
#foto_sin_pose = np.zeros(N_camaras,dtype=int) # Número de fotografías sin pose detectadas.
#error = np.zeros(N_camaras,dtype=float) # Número de fotografías con pose detectadas.

#cerrojo = threading.Lock()

# Informa si se detecta movimiento o no en la habitación.
def capturar_imagenes(id_camara, detectar_pose):
  global terminar
  directorio = "/var/www/html/images/" # root
  dir = "/home/ubuntu/pose/" # ubuntu

  fichero = dir + str(id_camara) + ".jpg"
#  ficheroA = directorio + str(id_camara) + ".jpg"
#  print("f: " + fichero)
  if os.path.exists(fichero):          # Cambiarlo a fichero
    os.system("rm -f "+fichero)

  ficheroB = directorio + str(camaras[id_camara][0]) + ".jpg"

  if detectar_pose:
    fichero_fondo=directorio + "fondo-"+ str(camaras[id_camara][0]) + ".jpg"
    if os.path.exists(fichero_fondo): 
      imagen_fondo = cv2.imread(fichero_fondo) ## leer imagen de fondo.
    else:
      if str(camaras[id_camara][3])!="robot":  # Robot Pepper no utiliza imagen de fondo fija, utiliza la misma imagen como fondo.
        print("No existen imágenes de fondo.")
        terminar = True

    ficheroC = directorio + str(camaras[id_camara][0]) + "_pose.jpg"

  # Comando A para descargar fichero de la Raspberry.
  comandoA="sshpass -p " + str(camaras[id_camara][5]) + " scp " + str(camaras[id_camara][4]) + "@" + str(camaras[id_camara][1]) + ":" + str(camaras[id_camara][2]) + " " + fichero

  # Comando B para mover fichero a la web.
#  comandoB="sudo mv " + fichero + ficheroA

  if str(camaras[id_camara][3])=="térmica":
    # Comando C para eliminar fichero de la Raspberry.
    comandoC="sshpass -p " + str(camaras[id_camara][5]) + " ssh " + str(camaras[id_camara][4]) + "@" + str(camaras[id_camara][1]) + " rm " + str(camaras[id_camara][2])

  while not terminar:
#    print(comandoA)
    res=os.system(comandoA) # Traer fotografía
    while res!=0: # Repetir hasta que no detecte error
      res=os.system(comandoA) # Traer fotografía

#    print(comandoB)
#    res=os.system(comandoB) # Mover fichero
#    while res!=0: # Repetir hasta que no detecte error
#      res=os.system(comandoB) # Mover fichero

    if str(camaras[id_camara][3])!="robot":
      print(comandoC)
      res=os.system(comandoC) 
      while res!=0: # Repetir hasta que no detecte error
        res=os.system(comandoC) 
    continuar = False
    while not continuar: 
      if os.path.exists(fichero): 
#        if not detectar_pose: # Mostrar en la web las imágenes capturadas de las cámaras.
#        print("pasa por B")
        os.system("sudo cp " + fichero + " " + ficheroB)
        if detectar_pose: # Mostrar en la web las imágenes capturadas de las cámaras.
#        else: # Mostrar en la web las poses.
#          print("pasa por A")
          imagen = cv2.imread(fichero) # leer imagen.
          mp_pose = mp.solutions.pose
          mp_drawing = mp.solutions.drawing_utils
          if str(camaras[id_camara][3])=="robot":
            imagen_fondo = imagen # leer imagen.
          fondo_con_pose = imagen_fondo.copy()
          with mp_pose.Pose(static_image_mode=IMAGENES_ESTATICAS, min_detection_confidence=DETECCION_MINIMA, min_tracking_confidence=SEGUIMIENTO_MINIMO) as pose: # model_complexity=2 solo funciona en equipo físico, no en MV.
            # Convertir la imagen BGR a RGB y analizarla con Pose de MediaPipe.
            marcas_pose = pose.process(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
            if marcas_pose.pose_landmarks: # Detectada pose en la imagen.
              mp_drawing.draw_landmarks(image=fondo_con_pose, landmark_list=marcas_pose.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)
#              print("Elimina: " + ficheroA)
              os.system("rm -f " + fichero)
#              if str(camaras[id_camara][3])!="robot":
#              cv2.imwrite(ficheroA, fondo_con_pose)
#              else:
              cv2.imwrite(fichero, fondo_con_pose)
              os.system("sudo cp " + fichero + " " + ficheroC)
            else:
              if str(camaras[id_camara][3])=="robot":
#                print("Copia: " + ficheroC)
                os.system("sudo cp " + fichero + " " + ficheroC)
#        print("Elmina2222")
        os.system("rm -f "+fichero)
        continuar = True

terminar = False
inicio = time.time()
#print("Inicio: " + str(inicio))  

if len(sys.argv) != 3 and len(sys.argv) != 4:
  print("Ejecutar: ")
  print("       sudo python3 podes_paginaweb.py id_camara tiempo [opción]")
  print("donde:")
  print("       id_camara = 0 (dormitorio), 1 (cocina), 2 (distribuidor), 3 (salón), 4 (TV), 5 (recibidor), 6 (aseo-térmica) y 7 (Pepper).")
  print("       tiempo = nº horas funcionando.")
  print("       opción = c (muestra imágenes), p (muestra poses) y f (toma imágenes de fondo).")
else:
  ID_camara = int(sys.argv[1]) # Selecciona la cámara especificada.
  print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "]: Creando hebra para obtener imágenes de las cámaras...")
  print("Pulsa la tecla:")
  print("   c para mostar en la web las imágenes capturadas de todas las cámaras.")
  print("   p para mostrar en la web las poses de todas las cámaras.")
  print("   f para tomar fotos del fondo.")
  print("   t para terminar el programa.")
  N_horas = int(sys.argv[2]) * 3600
  if len(sys.argv) == 4:
    opcion = sys.argv[3]
  while True:
    if len(sys.argv) != 4:
      opcion=input("\n¿Qué tecla deseas? ")
    if opcion == "c": # Muestra en la web las imágenes de las cámaras.
      # Ejecutar una hebra por cada cámara para detectar movimiento y hacer fotos.
      terminar = False
      print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "]: Capturando imágenes de " + str(camaras[ID_camara][0]) + ".")
#      for num_hilo in range(ID_camara, N_camaras, 1):
      hilo = threading.Thread(target=capturar_imagenes, args=(ID_camara, False), kwargs={})
      hilo.start()
      hebras.append(hilo)
    if opcion == "p": # Muestra en la web las imágenes de las cámaras.
      # Ejecutar una hebra por cada cámara para detectar movimiento y hacer fotos.
      terminar = False
      print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "]: Capturando pose de " + str(camaras[ID_camara][0]) + ".")
#      for num_hilo in range(ID_camara, N_camaras, 1):
      hilo = threading.Thread(target=capturar_imagenes, args=(ID_camara, True), kwargs={})
      hilo.start()
      hebras.append(hilo)
    if opcion == "f": # Obtiene imágenes de fondo.
      id_camara=ID_camara
      directorio='/var/www/html/images/'
#      print("dir: " + directorio + " ID_camara: " + str(ID_camara) + " N_camaras: " + str(N_camaras))
#      for id_camara in range(ID_camara, N_camaras, 1):
      print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "]: Creando imágenes de fondo de " + str(camaras[ID_camara][0]) + ".")
      # Desactivar que se muestre la marca de tiempo en las imágenes.
#      fichero_result=directorio + "resultado.txt"
#      wget.download(str(camaras[ID_camara][1])+comando_habilitar_marca_tiempo+"0",fichero_result)
#      time.sleep(10) 
#      if os.path.exists(fichero_result): 
#        os.system("chmod 770 "+fichero_result)
#        os.remove(fichero_result)
      fichero_fondo=directorio + "fondo-"+ str(camaras[ID_camara][0]) + ".jpg"
      if os.path.exists(fichero_fondo): 
        os.system("sudo rm -f "+fichero_fondo)
#        os.remove(fichero_fondo)
      # Comando A para descargar fichero de la Raspberry.
      comandoA="sshpass -p " + str(camaras[id_camara][5]) + " scp " + str(camaras[id_camara][4]) + "@" + str(camaras[ID_camara][1]) + ":" + str(camaras[id_camara][2]) + " /home/ubuntu/pose/" + str(ID_camara) + ".jpg"
      res=os.system(comandoA) # Traer fotografía
      while res!=0: # Repetir hasta que no detecte error
        res=os.system(comandoA) # Traer fotografía
      # Comando B para mover el fichero a la web.
      comandoB="sudo mv /home/ubuntu/pose/" + str(ID_camara) + ".jpg "+ fichero_fondo
      res=os.system(comandoB) # Mover fichero
      while res!=0: # Repetir hasta que no detecte error
        res=os.system(comandoB) # Mover fichero 
      if str(camaras[id_camara][3])=="térmica":
        # Comando C para eliminar fichero en la Raspberry.
        comandoC="sshpass -p " + str(camaras[id_camara][5]) + " ssh " + str(camaras[id_camara][4]) + "@" + str(camaras[ID_camara][1]) + " rm " + str(camaras[id_camara][2])
      if str(camaras[id_camara][3])!="robot":
        # Comando C copiamos la imagen descargada como fondo.
#        comandoC="sudo cp " + ficheroA + " " + fichero_fondo
        res=os.system(comandoC) 
        while res!=0: # Repetir hasta que no detecte error
          res=os.system(comandoC)
#      wget.download(str(camaras[ID_camara][1])+comando_hacer_fotos, fichero_fondo)
#      os.system("chmod 770 "+fichero_fondo)
      # Activar que se muestre la marca de tiempo en las imágenes.
#      wget.download(str(camaras[ID_camara][1])+comando_habilitar_marca_tiempo+"1",fichero_result)
#      time.sleep(10) 
#      if os.path.exists(fichero_result): 
#        os.system("chmod 770 "+fichero_result)
#        os.remove(fichero_result)
    if opcion == "t": # Termina la ejecución.
      print("Terminando...")
      terminar = True
      # Esperar a que terminen las hebras de las distintas cámaras.
      for hilo in hebras:
        hilo.join()
      break
    opcion=""
    duracion = time.time() - inicio
    if duracion >= N_horas: # Terminar al pasar el tiempo especificado.
      terminar = True
      # Esperar a que terminen las hebras de las distintas cámaras.
      for hilo in hebras:
        hilo.join()
      break;
sys.exit()
