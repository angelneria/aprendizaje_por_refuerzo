# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 12:51:54 2024

@author: Ángel
"""
import random
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
    @type mapa: list[list[int]]
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
    @type mapa: list[list[int]]
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
    @type mapa: list[list[int]]
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

def inicializa_tabla_q(acciones,numero_filas, numero_columnas):
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
            
    return tabla_q

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

def selecciona_estado_inicial(mapa, destino):
    """
    Selecciona un estado inicial válido en el mapa que no sea un obstáculo y no sea el destino.

    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @return: las coordenadas del estado inicial seleccionado
    @rtype: tuple(int, int)
    """
    numero_filas= len(mapa)
    numero_columnas = mapa[0].size
    coordenada_y = 0
    coordenada_x = 0
    
    while mapa[coordenada_y][coordenada_x]==1:
        coordenada_y = random.randint(0, numero_filas-1)
        coordenada_x = random.randint(0, numero_columnas-1)
    
    return ((coordenada_x,coordenada_y))
 
    
def accion_max_recompensa(estado, tabla_q):
    """
    Selecciona la acción que tiene la máxima recompensa para un estado dado, en caso de empate selecciona una aleatoria.

    @param estado: coordenadas del estado para el que se quiere seleccionar la acción
    @type estado: tuple(int, int)
    @param tabla_q: tabla Q que contiene las recompensas asociadas a las acciones para cada estado
    @type tabla_q: dict[tuple(int, int), dict[str, float]]
    @return: la acción con la máxima recompensa para el estado dado
    @rtype: str
    """
    acciones_recompensas = tabla_q.get(estado)
   
    recompensa_maxima = max(acciones_recompensas.values())
    acciones_maximas = [accion for accion, recompensa in acciones_recompensas.items() if recompensa == recompensa_maxima]
    accion_seleccionada = random.choice(acciones_maximas)

    return accion_seleccionada


def aplica_SARSA(mapa, destino, lista_acciones,lista_estados, numero_espisodios, recompensas, indices, alpha, gamma):
    """
    Aplica el algoritmo SARSA para encontrar la política de navegación óptima.

    @param mapa: matriz que representa el mapa donde 1 indica obstáculo y 0 indica espacio libre
    @type mapa: np.ndarray
    @param destino: coordenadas del destino (x, y)
    @type destino: tuple(int, int)
    @param lista_acciones: lista de acciones posibles ('N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO')
    @type lista_acciones: list[str]
    @param lista_estados: lista de estados navegables
    @type lista_estados: list[tuple(int, int)]
    @param numero_espisodios: número de episodios para ejecutar el algoritmo SARSA
    @type numero_espisodios: int
    @param recompensas: matriz de recompensas para el sistema de navegación
    @type recompensas: np.ndarray
    @param indices: diccionario que mapea acciones a índices en la matriz de recompensas
    @type indices: dict[str, int]
    @param alpha: tasa de aprendizaje
    @type alpha: float
    @param gamma: factor de descuento para las recompensas futuras
    @type gamma: float
    @return: None
    """
    
    numero_filas= len(mapa)
    numero_columnas = mapa[0].size
    
    politica_inicial= inicializa_politica(numero_filas, numero_columnas, destino, lista_acciones)
    tabla_q = inicializa_tabla_q(lista_acciones, numero_filas, numero_columnas)
    

    
    for episodio in range(numero_espisodios):
        estado_inicial= selecciona_estado_inicial(mapa, destino)
        accion_inicial= accion_max_recompensa(estado_inicial, tabla_q)
        
        
        while(estado_inicial != destino):
            
            coordenada_x= estado_inicial[0]
            coordenada_y= estado_inicial[1]
            recompensa = recompensas[numero_filas*coordenada_x + coordenada_y][indices[accion_inicial]]
            
            if(accion_inicial!='esperar'):
                errores_de_accion = obtiene_posibles_errores(accion_inicial)
                acciones_con_errores = [accion_inicial] + errores_de_accion
                accion_tomada = np.random.choice(acciones_con_errores,p=[0.8,0.1,0.1])
            else:
                accion_tomada = accion_inicial
                    
                
            estado_actual= aplica_accion(estado_inicial, accion_tomada, mapa)
            accion_a_tomar = accion_max_recompensa(estado_actual, tabla_q)
            
            tabla_q[estado_inicial][accion_inicial] = tabla_q[estado_inicial][accion_inicial] + alpha*(recompensa+gamma*tabla_q[estado_actual][accion_a_tomar]-tabla_q[estado_inicial][accion_inicial])
           
            
            if not hay_colision(estado_actual, mapa):
                estado_inicial= estado_actual            
            accion_inicial= accion_a_tomar
    
    mejores_acciones  = {}
    for estado, acciones in tabla_q.items():
        if(estado != destino):
            mejores_acciones[estado] = accion_max_recompensa(estado,tabla_q)


    for estado, mejor_accion_tomada in mejores_acciones.items():
        politica_inicial[estado[1]][estado[0]] = mejor_accion_tomada
    
    politica_para_lectura=leer_por_columnas(politica_inicial)
    visualiza_politica(politica_para_lectura, lista_estados, mapa, destino)
    
        
        
        
