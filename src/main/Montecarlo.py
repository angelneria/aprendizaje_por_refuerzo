# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 11:02:55 2024

@author: Angel
"""
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

def lee_mapa(fichero):
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
    plt.figure(figsize=(len(mapa[0]), len(mapa)))
    plt.imshow(1-mapa, cmap='gray', interpolation='none')
    plt.xlim(-0.5, len(mapa[0]) - 0.5)
    plt.ylim(-0.5, len(mapa) - 0.5)
    plt.gca().add_patch(plt.Circle(destino,radius = 0.5,edgecolor = 'red', facecolor = 'red'))
    
def inicializa_politica(numero_filas, numero_columnas, destino, lista_acciones):
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
    tabla_q = {}
    for x in range(numero_columnas):
        for y in range(numero_filas):
            tabla_q[(x, y)] = {accion: 0 for accion in acciones}
            
    objetivo = (destino[0], destino[1])
    tabla_q[objetivo] = {accion: None for accion in acciones}
    return tabla_q

def inicializa_tabla_Racum(acciones,numero_filas, numero_columnas, destino):
    tabla_Racum = {}
    for x in range(numero_columnas):
        for y in range(numero_filas):
            tabla_Racum[(x, y)] = {accion: [] for accion in acciones}
            
    objetivo = (destino[0], destino[1])
    tabla_Racum[objetivo] = {accion: None for accion in acciones}
    return tabla_Racum

def genera_estados(mapa):
    nav_estados = []
    for i in range(0,mapa.shape[1]):
        for j in range(0,mapa.shape[0]):
            nav_estados.append(tuple([i,j]))
    return nav_estados

def hay_colision(estado, mapa):
    return mapa[estado[1],estado[0]]==1

def aplica_accion(estado,accion, mapa):
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
        

def obtiene_posibles_errores(accion):
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

def crea_recompensas_sistema(nav_estados, nav_acciones, destino, mapa, k1, k2):
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


def obtiene_recompensa(estado, destino,mapa, K= 1000):
    if hay_colision(estado, mapa):
        valor = -K
  
    else:
        valor = - (abs(estado[0]-destino[0]) + abs(estado[1]-destino[1]))
    return valor
    
def aplica_Montecarlo(mapa, destino, lista_acciones, estado_inicial, numero_espisodios, factor_descuento, recompensas, indices):
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
                print('Accion random:'+ accion_aleatoria + ', Accion tomada:' + accion_tomada)
            else:
                accion_tomada = accion_aleatoria
                acciones_tomadas.append(accion_tomada)
                print('Accion random:'+ accion_aleatoria + ', Accion tomada:' + accion_tomada)

            nuevo_estado = aplica_accion(estado_actual, accion_tomada, mapa)
            if not hay_colision(nuevo_estado, mapa):
                estado_actual= nuevo_estado
            print(f'Estado tras la accion: {estado_actual}')
        
        for estado in range(len(estados_recorridos)):
            U=0
            for subrecorrido in range(estado, len(estados_recorridos)):
                coordenada_x = estados_recorridos[estado][0]
                coordenada_y = estados_recorridos[estado][1]
                U+= (factor_descuento**(subrecorrido-estado)) * recompensas[numero_filas*coordenada_x + coordenada_y][indices[acciones_tomadas[estado]]]
            
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
             
    print(politica_inicial)
    return politica_inicial
    



def visualiza_politica(politica, nav_estados, mapa, destino):
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
    
    
def leer_por_columnas(politica):
    politica_forma_matriz = np.array(politica)
    politica_transpuesta = politica_forma_matriz.T
    resultado = []
    for columna in politica_transpuesta:
        resultado.extend(columna) #forma una lista con los valores de cada columna
    return resultado



mapa, destino = lee_mapa("mapa3.txt")
estado_actual=(2,4)
lista_acciones = ['esperar','N','NE','E','SE','S','SO','O','NO']
indices_nav_acciones = {'esperar': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5, 'SO': 6, 'O': 7, 'NO': 8}


nav_estados3 = genera_estados(mapa)

nav_recompensas_sistema = crea_recompensas_sistema(nav_estados3, lista_acciones, destino, mapa, 1000, 100)

politca_obtenida_montecarlo = aplica_Montecarlo(mapa, destino, lista_acciones, estado_actual,100, 0.9, nav_recompensas_sistema, indices_nav_acciones)


politicaBuena=leer_por_columnas(politca_obtenida_montecarlo)

print(nav_estados3)
print()
print(politicaBuena)

visualiza_politica(politicaBuena, nav_estados3, mapa, destino)
