
import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX

def nothing(x):
    return

def Cuadra (v1, v2, rng):
	suma = 0
	for i in range(rng):
		suma = suma + (v1[i-1]-v2[i-1])**2
	res = (suma/rng) ** 0.5
	return res


def DefinirFormato(x1,x2,x3,x4,x5,x6,x7,nombre):
#Definicion variables
    coincidencias = 1
    bines = 64 #bines para histogramas


# Creamos controles de ajuste
    cv2.namedWindow('Horizontal')

# Crearemos los controles para indicar tamaño contorno
    cv2.createTrackbar('H maximo', 'Horizontal', x1, 480, nothing)
    cv2.createTrackbar('Altura', 'Horizontal', x2, 460, nothing)
    cv2.createTrackbar('Ancho', 'Horizontal', x3, 400, nothing)
    cv2.createTrackbar('Ubicacion1', 'Horizontal', x4, 640, nothing)
    cv2.createTrackbar('Ubicacion2', 'Horizontal', x5, 640, nothing)
    cv2.createTrackbar('Ubicacion3', 'Horizontal', x6, 640, nothing)
    cv2.createTrackbar('umbral', 'Horizontal', x7, 5640, nothing)


# Crea variable de camara y asiga la primera camara disponible con "0"
  #  cap = cv2.VideoCapture('http://192.168.1.44:4747/video')
    cap = cv2.VideoCapture(0)
    cv2.waitKey(50)
#cap = cv2.VideoCapture('http://172.20.10.2:4747/video')

# Iniciamos el bucle de captura, en el que leemos cada frame de la captura
    while (True):
    
    # Capturamos imagen
        ret, frame = cap.read()
    
    # Ajustamos rectangulos
        Hmax = cv2.getTrackbarPos('H maximo', 'Horizontal')
        Altura = cv2.getTrackbarPos('Altura', 'Horizontal')
        Ancho = cv2.getTrackbarPos('Ancho', 'Horizontal')
        Ubicacion1 = cv2.getTrackbarPos('Ubicacion1', 'Horizontal')
        Ubicacion2 = cv2.getTrackbarPos('Ubicacion2', 'Horizontal')
        Ubicacion3 = cv2.getTrackbarPos('Ubicacion3', 'Horizontal')
        umbral = cv2.getTrackbarPos('umbral', 'Horizontal')

    #Recortes
        recorte1 = frame [Hmax-Altura:Hmax, Ubicacion1:Ubicacion1+Ancho]
        recorte2 = frame [Hmax-Altura:Hmax, Ubicacion2:Ubicacion2+Ancho]
        recorte3 = frame [Hmax-Altura:Hmax, Ubicacion3:Ubicacion3+Ancho]

    #Dibuja rectangulos
        cv2.rectangle(frame, (Ubicacion1,Hmax-Altura),(Ubicacion1+Ancho,Hmax),(255,0,0),1)
        cv2.rectangle(frame, (Ubicacion2,Hmax-Altura),(Ubicacion2+Ancho,Hmax),(255,0,0),1)
        cv2.rectangle(frame, (Ubicacion3,Hmax-Altura),(Ubicacion3+Ancho,Hmax),(255,0,0),1)

    #Obtenemos histogramas
        his1blu = cv2.calcHist([recorte1], [0], None, [bines], [0,256])
        his1gre = cv2.calcHist([recorte1], [1], None, [bines], [0,256])
        his1red = cv2.calcHist([recorte1], [2], None, [bines], [0,256])
        his2blu = cv2.calcHist([recorte2], [0], None, [bines], [0,256])
        his2gre = cv2.calcHist([recorte2], [1], None, [bines], [0,256])
        his2red = cv2.calcHist([recorte2], [2], None, [bines], [0,256])
        his3blu = cv2.calcHist([recorte3], [0], None, [bines], [0,256])
        his3gre = cv2.calcHist([recorte3], [1], None, [bines], [0,256])
        his3red = cv2.calcHist([recorte3], [2], None, [bines], [0,256])

    #Calculo de diferencias cuadraticas
        dif12 = Cuadra (his1blu, his2blu, bines) + Cuadra (his1gre, his2gre, bines) + Cuadra (his1red, his2red, bines)
        dif13 = Cuadra (his1blu, his3blu, bines) + Cuadra (his1gre, his3gre, bines) + Cuadra (his1red, his3red, bines)
        dif32 = Cuadra (his3blu, his2blu, bines) + Cuadra (his3gre, his2gre, bines) + Cuadra (his3red, his2red, bines)
    
    #Vemos cantidad de observaciones seguidas que cumplen
        if dif12 < umbral and dif13 < umbral and dif32 < umbral:
            if coincidencias < 8:
              coincidencias = coincidencias + 1
        else:
            if coincidencias > 1:
              coincidencias = coincidencias - 1

    #Dibujamos luz verde o roja
        if coincidencias > 3:
            cv2.rectangle(frame,(600,10),(630,40),(0,255,0),-1)
        else:
            cv2.rectangle(frame,(600,10),(630,40),(0,0,255),-1)

        cv2.putText(frame,str(int(dif12)), (10,40), font, 1, 255)
        cv2.putText(frame,str(int(dif13)), (110,40), font, 1, 255)
        cv2.putText(frame,str(int(dif32)), (210,40), font, 1, 255)
        cv2.putText(frame,str(coincidencias), (310,40), font, 1, 255)
        cv2.putText(frame,"Presione q para terminar",(10,400),font,1,255)

    # Creamos las ventanas de salidam y configuracion
        cv2.imshow('Original', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Indicamos que al pulsar "q" el programa se cierre
            break

        


# Guardamos variables en archivo de configuracion
    cv2.destroyAllWindows()
    
    archivo = open(str((nombre)+".txt"),"a")
    archivo.write(str(Hmax)+"\n"+str(Altura)+"\n"+str(Ancho)+"\n"+str(Ubicacion1)+"\n"+str(Ubicacion2)+"\n"+
                  str(Ubicacion3)+"\n"+str(umbral))
    archivo.close()

    

# Nombre de las variables
#  Hmax ('H maximo', 'Horizontal')
#  Altura ('Altura', 'Horizontal')
#  Ancho ('Ancho', 'Horizontal')
#  Ubicacion1 ('Ubicacion1', 'Horizontal')
#  Ubicacion2 ('Ubicacion2', 'Horizontal')
#  Ubicacion3 ('Ubicacion3', 'Horizontal')
#  umbral = cv2.getTrackbarPos('umbral', 'Horizontal')