import cv2
import numpy as np

#Para cv2 los valores se toman como [azul,verde, rojo]
def carga_pixeles():
    '''
    Funcion que dados los valores del archivo "Dibujo.txt" lee
    los valores y los almacena en un arreglo de numpy con formato
    BGR que representa pixeles
    :return: El arreglo de numpy con dimensiones 100*100*3
    '''
    archivo =open("Dibujo.txt",'r')
    numeros = []
    for linea in archivo:
        linea = linea.replace('\n', " ")
        num = linea.split(' ')
        for n in num:
            if n.isdigit():
                #Guardamos los numeros en el arreglo
                numeros.append(int(n))
    #Transformamos nuestro arreglo a uno de numpy
    x = np.array(numeros)
    x = np.reshape(x,(100,100,3))
    # El dibujo original esta en RGB y lo pasamos a BGR
    x[:,:, 0], x[:,:, 2] = x[:,:, 2], x[:,:, 0].copy()
    return x

def grafica(r_ojos, g_ojos, b_ojos,r_tez,g_tez,b_tez,r_cab,g_cab,b_cab,nombre_imagen='imagen_act.png'):
    '''
    Funcion que dados los valores de tez, ojos y cabello, genera la imagen
    y la guarda con nombre "imagen_act.png" por default
    :param r_ojos: Parametro de rojo de los ojos
    :param g_ojos: Parametro de verde de los ojos
    :param b_ojos: Parametro de azul de los ojos
    :param r_tez: Parametro de rojo de la tez
    :param g_tez: Parametro de verde de la tez
    :param b_tez: Parametro de azul de la tez
    :param r_cab: Parametro de rojo del cabello
    :param g_cab: Parametro de verde del cabello
    :param b_cab: Parametro de azul del cabello
    :param nombre_imagen: Nombre para guardar la imagen
    '''
    dibujo = carga_pixeles()
    for i in range(0,dibujo.shape[0]):
        for j in range(0,dibujo.shape[1]):
            # Cambiamos la tez
            if dibujo[i,j][2] == 249 and dibujo[i,j][1] == 235 and dibujo[i,j][0]  == 169:
                dibujo[i, j][0], dibujo[i, j][1], dibujo[i, j][2] = b_tez, g_tez, r_tez
            #Cambiamos cabello
            elif dibujo[i,j][2] == 47 and dibujo[i,j][1] == 0 and dibujo[i,j][0]  == 255:
                dibujo[i, j][0], dibujo[i, j][1], dibujo[i, j][2] = b_cab, g_cab, r_cab
            # Cambiamos los ojos
            elif dibujo[i,j][2] == 60 and dibujo[i,j][1] == 197 and dibujo[i,j][0]  == 217:
                dibujo[i, j][0], dibujo[i, j][1], dibujo[i, j][2] = b_ojos, g_ojos, r_ojos
    cv2.imwrite(nombre_imagen, dibujo)

