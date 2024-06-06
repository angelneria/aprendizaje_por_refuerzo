# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 11:02:55 2024

@author: Angel
"""
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

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
    Función que aplica una acción al estado actual para obtener un nuevo estado, en caso de colisión se devuelve el mismo estado.

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
        if accion=='esperar' or accion =='X':
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


def inicializa_politica(numero_filas, numero_columnas, destino, lista_acciones):
    """
    Inicializa la política de navegación con acciones aleatorias para cada estado, excepto el destino.

    @param numero_filas: número de filas del mapa
    @type numero_filas: int
    @param numero_columnas: número de columnas del mapa
    @type numero_columnas: int
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @param lista_acciones: lista de acciones posibles ('N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO')
    @type lista_acciones: list[str]
    @return: matriz de políticas inicializada
    @rtype: list[list[str]]
    """

    politica_inicial= np.empty((numero_filas, numero_columnas), dtype='U10')
    for x in range(numero_filas):
        for y in range(numero_columnas):
            if (x==destino[1] and y==destino[0]):
                politica_inicial[x,y]= 'X'
            else:
                accion = random.choice(lista_acciones)
                politica_inicial[x,y]= accion
    return politica_inicial

def inicializa_tabla_q(acciones,numero_filas, numero_columnas, destino):
    """
    Inicializa la tabla Q con valores cero para cada par de estado-acción, excepto para el estado objetivo.

    @param acciones: lista de acciones posibles ('N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO')
    @type acciones: list[str]
    @param numero_filas: número de filas del mapa
    @type numero_filas: int
    @param numero_columnas: número de columnas del mapa
    @type numero_columnas: int
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @return: tabla Q inicializada
    @rtype: dict[tuple(int, int), dict[str, int]]
    """
    tabla_q = {}
    for x in range(numero_columnas):
        for y in range(numero_filas):
            tabla_q[(x, y)] = {accion: 0 for accion in acciones}
            
    objetivo = (destino[0], destino[1])
    tabla_q[objetivo] = {accion: None for accion in acciones}
    return tabla_q

def inicializa_tabla_Racum(acciones,numero_filas, numero_columnas, destino):
    """
    Inicializa la tabla de recompensas acumuladas con listas vacías para cada par de estado-acción, 
    excepto para el estado objetivo.

    @param acciones: lista de acciones posibles ('N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO')
    @type acciones: list[str]
    @param numero_filas: número de filas del mapa
    @type numero_filas: int
    @param numero_columnas: número de columnas del mapa
    @type numero_columnas: int
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @return: tabla de recompensas acumuladas inicializada
    @rtype: dict[tuple(int, int), dict[str, list]]
    """
    tabla_Racum = {}
    for x in range(numero_columnas):
        for y in range(numero_filas):
            tabla_Racum[(x, y)] = {accion: [] for accion in acciones}
            
    objetivo = (destino[0], destino[1])
    tabla_Racum[objetivo] = {accion: None for accion in acciones}
    return tabla_Racum

def leer_por_columnas(politica):
    """
    Lee la política de navegación por columnas en lugar de por filas.

    @param politica: matriz de políticas de navegación
    @type politica: list[list[str]]
    @return: política de navegación leída por columnas
    @rtype: list[str]
    """
    politica_forma_matriz = np.array(politica)
    politica_transpuesta = politica_forma_matriz.T
    resultado = []
    for columna in politica_transpuesta:
        resultado.extend(columna) 
    return resultado


def aplica_Montecarlo(mapa, destino, lista_acciones,lista_estados, estado_inicial, numero_espisodios, factor_descuento, recompensas, indices, primera_visita=False):
    """
    Aplica el algoritmo de Montecarlo para encontrar la política de navegación óptima.

    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @param lista_acciones: lista de acciones posibles ('N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO')
    @type lista_acciones: list[str]
    @param lista_estados: lista de estados navegables
    @type lista_estados: list[tuple(int, int)]
    @param estado_inicial: coordenadas del estado inicial (x, y)
    @type estado_inicial: tuple(int, int)
    @param numero_espisodios: número de episodios para ejecutar el algoritmo de Montecarlo
    @type numero_espisodios: int
    @param factor_descuento: factor de descuento para las recompensas futuras
    @type factor_descuento: float
    @param recompensas: matriz de recompensas para el sistema de navegación
    @type recompensas: np.ndarray
    @param indices: diccionario que mapea acciones a índices en la matriz de recompensas
    @type indices: dict[str, int]
    @param primera_visita: indica si se debe utilizar el método de primera visita para el algoritmo de Montecarlo
    @type primera_visita: bool
    @return: None
    """
    numero_filas= len(mapa)
    numero_columnas = mapa[0].size
    
    politica_inicial= inicializa_politica(numero_filas, numero_columnas, destino, lista_acciones)
    
    tabla_q = inicializa_tabla_q(lista_acciones, numero_filas, numero_columnas, destino)
    
    tabla_Racum = inicializa_tabla_Racum(lista_acciones, numero_filas, numero_columnas, destino)
    
    for episodio in range(numero_espisodios):
        estado_actual = estado_inicial
        
        estados_recorridos =[]
        acciones_tomadas= []
        
        while estado_actual != destino:
            estados_recorridos.append(estado_actual)
            accion_aleatoria = random.choice(lista_acciones)
            accion_tomada = ''
            if(accion_aleatoria!= 'esperar'):
                errores_de_accion = obtiene_posibles_errores(accion_aleatoria)
                acciones_con_errores = [accion_aleatoria] + errores_de_accion
                accion_tomada = np.random.choice(acciones_con_errores,p=[0.8,0.1,0.1])
                acciones_tomadas.append(accion_tomada)
            else:
                accion_tomada = accion_aleatoria
                acciones_tomadas.append(accion_tomada)

            nuevo_estado = aplica_accion(estado_actual, accion_tomada, mapa)
            if not hay_colision(nuevo_estado, mapa):
                estado_actual= nuevo_estado
        
        tuplas_estados_y_acciones_recorridos=[]
        
        for estado in range(len(estados_recorridos)):
            U=0
            estado_en_curso =estados_recorridos[estado]
            accion_en_curso = acciones_tomadas[estado]
            
            
            for subrecorrido in range(estado, len(estados_recorridos)):
                
                coordenada_x = estados_recorridos[estado][0]
                coordenada_y = estados_recorridos[estado][1]
                U+= (factor_descuento**(subrecorrido-estado)) * recompensas[numero_filas*coordenada_x + coordenada_y][indices[acciones_tomadas[estado]]]
                
            if (primera_visita==False or (estado_en_curso, accion_en_curso) not in tuplas_estados_y_acciones_recorridos):
                tuplas_estados_y_acciones_recorridos.append((estado_en_curso, accion_en_curso))
                tabla_Racum[estados_recorridos[estado]][acciones_tomadas[estado]].append(U)
                lista_valores = tabla_Racum[estados_recorridos[estado]][acciones_tomadas[estado]]
                media = sum(lista_valores)/len(lista_valores)
                tabla_q[estados_recorridos[estado]][acciones_tomadas[estado]] = media
            
        
        mejores_acciones  = {}
        for estado, acciones in tabla_q.items():
            if(estado != destino):
                recompensa_maxima = max(acciones.values())
                mejores_acciones_para_estado = [accion for accion, recompensa_accion in acciones.items() if recompensa_accion == recompensa_maxima]
                mejor_accion = random.choice(mejores_acciones_para_estado)
                mejores_acciones[estado] = mejor_accion


        for estado, mejor_accion_tomada in mejores_acciones.items():
            politica_inicial[estado[1]][estado[0]] = mejor_accion_tomada
        
        print(f'Episodio {episodio +1} terminado')
             
    politica_para_lectura=leer_por_columnas(politica_inicial)
    visualiza_politica(politica_para_lectura, lista_estados, mapa, destino)
    



    
    





