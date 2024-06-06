# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:44:29 2024

@author: manue
"""
import mdptoolbox.mdp as mdp
import numpy as np
import matplotlib.pyplot as plt

########################################### FUNCIONES GENERALES ###########################################

def lee_mapa(fichero):
    '''
    Función que lee un fichero de texto que contiene una matriz de enteros y dos números flotantes.
    
    @param fichero: nombre del fichero que contiene los datos
    @type fichero: str
    @return: una tupla que contiene una matriz numpy de enteros (el mapa) y una tupla con dos flotantes (destino)
    @rtype: tuple (np.ndarray, tuple(float, float))
    '''
    with open(fichero,'r') as archivo:
        lineas = archivo.readlines()
    numeros = [float(numero) for numero in lineas[0].split()]
    lineas.pop(0)
    lineas.reverse()
    matriz = []
    for linea in lineas:
        fila = [int(caracter) for caracter in linea.strip()]
        matriz.append(fila)
    return np.array(matriz),(numeros[0],numeros[1])

def visualiza_mapa(mapa, destino):
    '''
    Función que visualiza un mapa en escala de grises y marca un destino con un círculo rojo.
    
    @param mapa: la matriz que representa el mapa
    @type mapa: np.ndarray
    @param destino: coordenadas del destino en el mapa
    @type destino: tuple (int, int)
    @return: None
    '''
    plt.figure(figsize=(len(mapa[0]), len(mapa)))
    plt.imshow(1-mapa, cmap='gray', interpolation='none')
    plt.xlim(-0.5, len(mapa[0]) - 0.5)
    plt.ylim(-0.5, len(mapa) - 0.5)
    plt.gca().add_patch(plt.Circle(destino,radius = 0.5,edgecolor = 'red', facecolor = 'red'))
    
    

def genera_estados(mapa):
    '''
    Función que genera una lista de estados navegables a partir de un mapa.

    @param mapa: la matriz que representa el mapa
    @type mapa: np.ndarray
    @return: lista de estados navegables como tuplas de coordenadas (x, y)
    @rtype: list of tuple(int, int)
    '''
    nav_estados = []
    for i in range(0,mapa.shape[1]):
        for j in range(0,mapa.shape[0]):
            nav_estados.append(tuple([i,j]))
    return nav_estados

def hay_colision(estado, mapa):
    """
    Función que determina si hay colisión en la posición dada en el mapa.

    @param estado: coordenadas del estado actual (x, y)
    @type estado: tuple(int, int)
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @return: True si hay colisión, False si no la hay
    @rtype: bool
    """
    return mapa[estado[1],estado[0]]==1


def obtiene_recompensa(estado, destino,mapa, K= 1000):
    """
    Función que obtiene la recompensa para un estado dado, considerando la colisión
    y la distancia al destino.

    @param estado: coordenadas del estado actual (x, y)
    @type estado: tuple(int, int)
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @param K: factor de penalización por colisión, por defecto 1000
    @type K: int
    @return: valor de la recompensa para el estado dado
    @rtype: int
    """
    if hay_colision(estado, mapa):
        valor = -K
  
    else:
        valor = - (abs(estado[0]-destino[0]) + abs(estado[1]-destino[1]))
    return valor


def aplica_accion(estado,accion, mapa):
    """
    Función que aplica una acción al estado actual para obtener un nuevo estado.

    @param estado: coordenadas del estado actual (x, y)
    @type estado: tuple(int, int)
    @param accion: acción a aplicar ('N': norte, 'S': sur, 'E': este, 'O': oeste,
                   'NE': noreste, 'SE': sureste, 'SO': suroeste, 'NO': noroeste)
    @type accion: str
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @return: nuevas coordenadas del estado después de aplicar la acción
    @rtype: tuple(int, int)
    """
    if hay_colision(estado, mapa):
        return estado
    x = estado[0]
    y = estado[1]
    
    if accion == 'N':
        y += 1
    elif accion == 'S':
        y -= 1
    elif accion == 'E':
        x += 1
    elif accion == 'O':
        x -= 1
    elif accion == 'NE':
        y += 1
        x += 1
    elif accion == 'SE':
        y -= 1
        x += 1
    elif accion == 'SO':
        y -= 1
        x -= 1
    elif accion == 'NO':
        y += 1
        x -= 1
    return x,y
        

def visualiza_politica(politica, nav_estados, mapa, destino):
    """
    Visualiza la política de navegación sobre el mapa, con flechas que representan las acciones tomadas.

    @param politica: lista de acciones correspondientes a cada estado en nav_estados
    @type politica: list[str]
    @param nav_estados: lista de estados navegados
    @type nav_estados: list[tuple(int, int)]
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @return: None
    """
    visualiza_mapa(mapa, destino)
    for p in zip(nav_estados,politica):
        accion = p[1]
        if accion=='esperar':
            continue
        estado = p[0]
        e1 = aplica_accion(estado,accion, mapa)
        x0 = estado[0]
        y0 = estado[1]
        x1 = e1[0]
        y1 = e1[1]
        
        plt.gca().arrow(x0, y0, (x1 - x0)*0.6, (y1 - y0)*0.6,
         head_width=0.3, head_length=0.3, fc='black', ec='black')
        
        
        
def crea_recompensas_sistema(nav_estados, nav_acciones, destino, mapa, k1, k2):
    """
    Crea la matriz de recompensas para el sistema de navegación.

    @param nav_estados: lista de estados navegados
    @type nav_estados: list[tuple(int, int)]
    @param nav_acciones: lista de acciones tomadas en cada estado
    @type nav_acciones: list[str]
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @param k1: factor de penalización por colisión en obtiene_recompensa
    @type k1: int
    @param k2: factor de penalización por no esperar no siendo el destino en crea_recompensas_sistema
    @type k2: int
    @return: matriz de recompensas para el sistema de navegación
    @rtype: np.ndarray
    """
    matriz = []
    for e in nav_estados:
       
        fila=[]
        for a in nav_acciones:
            next_e = aplica_accion(e, a, mapa)
            r= obtiene_recompensa(next_e, destino, mapa, k1)
            fila.append(r)
        if e != destino:
            fila[0]=-k2
        matriz.append(fila)
    return np.array(matriz)

def obtiene_posibles_errores(accion):
    """
    Obtiene las posibles acciones que pueden ser consideradas errores dada una acción.

    @param accion: acción principal ('N', 'S', 'E', 'O', 'NE', 'NO', 'SE', 'SO')
    @type accion: str
    @return: lista de acciones que son posibles errores para la acción dada
    @rtype: list[str]
    """
    if accion=='N':
        errores = ['NE','NO']
    elif accion=='S':
        errores = ['SE','SO']
    elif accion=='E':
        errores = ['NE','SE']
    elif accion=='O':
        errores = ['NO', 'SO']
    elif accion=='NE':
        errores = ['N','E']
    elif accion=='NO':
        errores = ['N','O']
    elif accion=='SE':
        errores = ['S','E']
    elif accion == 'SO':
        errores = ['S','O']
    else:
        errores = []
    return errores


########################################### FUNCIONES ESPECIFICAS ###########################################

def obtiene_indice_estado(estado, mapa):
    """
    Obtiene el índice del estado en la representación lineal del mapa.

    @param estado: coordenadas del estado actual (x, y)
    @type estado: tuple(int, int)
    @param mapa: matriz que representa el mapa
    @type mapa: np.ndarray
    @return: índice del estado en la representación lineal del mapa
    @rtype: int
    """
    return int(estado[0]*mapa.shape[0]+estado[1])


def crea_transiciones_movimiento(accion, prob_error, nav_estados, mapa):
    """
    Crea la matriz de transiciones para un movimiento dado con posibles errores.

    @param accion: acción principal ('N', 'S', 'E', 'O', 'NE', 'NO', 'SE', 'SO')
    @type accion: str
    @param prob_error: probabilidad de que ocurra un error al ejecutar la acción
    @type prob_error: float
    @param nav_estados: lista de estados navegados
    @type nav_estados: list[tuple(int, int)]
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @return: matriz de transiciones para el movimiento dado
    @rtype: np.ndarray
    """
    matriz = []
    for e0 in nav_estados:
        fila = [0]*len(nav_estados)
        if hay_colision(e0, mapa):
            fila[obtiene_indice_estado(e0, mapa)]=1
        else:
            goal = aplica_accion(e0,accion, mapa)
            errores = obtiene_posibles_errores(accion)
            if len(errores)==0:
                fila[obtiene_indice_estado(goal, mapa)] = 1
            else:
                fila[obtiene_indice_estado(goal, mapa)] = 1 - prob_error
                for error in errores:
                    goal_error = aplica_accion(e0,error, mapa)
                    fila[obtiene_indice_estado(goal_error, mapa)] = prob_error/len(errores)
        matriz.append(fila)
    return np.array(matriz)


def crea_transiciones_sistema(prob_error, nav_estados, mapa):
    """
    Crea la matriz de transiciones para el sistema de navegación.

    @param prob_error: probabilidad de que ocurra un error al ejecutar una acción
    @type prob_error: float
    @param nav_estados: lista de estados navegados
    @type nav_estados: list[tuple(int, int)]
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @return: matriz de transiciones para el sistema de navegación
    @rtype: np.ndarray
    """
    return np.array([crea_transiciones_movimiento('esperar',prob_error, nav_estados, mapa), 
                     crea_transiciones_movimiento('N',prob_error, nav_estados, mapa),
                     crea_transiciones_movimiento('NE',prob_error, nav_estados, mapa),
                     crea_transiciones_movimiento('E',prob_error, nav_estados, mapa),
                     crea_transiciones_movimiento('SE',prob_error, nav_estados, mapa),
                     crea_transiciones_movimiento('S',prob_error, nav_estados, mapa),
                     crea_transiciones_movimiento('SO',prob_error, nav_estados, mapa),
                     crea_transiciones_movimiento('O',prob_error, nav_estados, mapa),
                     crea_transiciones_movimiento('NO',prob_error, nav_estados, mapa)])

def aplica_Qlearning(factor_descuento, nav_transiciones_sistema, nav_recompensas_sistema, nav_acciones, nav_estados, mapa, destino, iteraciones):
    """
    Aplica el algoritmo Q-Learning para encontrar la política de navegación óptima.

    @param factor_descuento: factor de descuento para las recompensas futuras
    @type factor_descuento: float
    @param nav_transiciones_sistema: matriz de transiciones para el sistema de navegación
    @type nav_transiciones_sistema: np.ndarray
    @param nav_recompensas_sistema: matriz de recompensas para el sistema de navegación
    @type nav_recompensas_sistema: np.ndarray
    @param nav_acciones: lista de acciones posibles ('N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO')
    @type nav_acciones: list[str]
    @param nav_estados: lista de estados navegados
    @type nav_estados: list[tuple(int, int)]
    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @param iteraciones: número de iteraciones para ejecutar el algoritmo Q-Learning
    @type iteraciones: int
    @return: None
    """
    np.random.seed(1000)
    ejemplo_nav_robot = mdp.QLearning(
    transitions=nav_transiciones_sistema,
    reward=nav_recompensas_sistema,
    discount= factor_descuento,
    n_iter= iteraciones
    )
    ejemplo_nav_robot.setVerbose()
    ejemplo_nav_robot.run()
    nav_politica = [nav_acciones[i] for i in ejemplo_nav_robot.policy]
    visualiza_politica(nav_politica, nav_estados, mapa, destino)

    

            
