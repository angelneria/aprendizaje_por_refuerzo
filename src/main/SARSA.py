# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 12:51:54 2024

@author: Ángel
"""
import random
import numpy as np

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

def inicializa_tabla_q(acciones,numero_filas, numero_columnas, destino):
    tabla_q = {}
    for x in range(numero_columnas):
        for y in range(numero_filas):
            tabla_q[(x, y)] = {accion: 0 for accion in acciones}
            
    objetivo = (destino[0], destino[1])
    tabla_q[objetivo] = {accion: None for accion in acciones}
    return tabla_q

def selecciona_estado_inicial(mapa, destino):
    numero_filas= len(mapa)
    numero_columnas = mapa[0].size
    coordenada_y = 0
    coordenada_x = 0
    
    while mapa[coordenada_y][coordenada_x]==1:
        coordenada_y = random.randint(0, numero_filas-1)
        coordenada_x = random.randint(0, numero_columnas-1)
    
    return ((coordenada_x,coordenada_y))
 
    
def accion_max_recompensa(estado, tabla_q):
    acciones_recompensas = tabla_q.get(estado, {})
    recompensa_maxima = max(acciones_recompensas.values())
    acciones_maximas = [accion for accion, recompensa in acciones_recompensas.items() if recompensa == recompensa_maxima]
    accion_seleccionada = random.choice(acciones_maximas)

    return accion_seleccionada

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

def genera_estados(mapa):
    nav_estados = []
    for i in range(0,mapa.shape[1]):
        for j in range(0,mapa.shape[0]):
            nav_estados.append(tuple([i,j]))
    return nav_estados

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


def aplica_SARSA(mapa, destino, lista_acciones, numero_espisodios, recompensas, indices, alpha, gamma):
    
    numero_filas= len(mapa)
    numero_columnas = mapa[0].size
        
    tabla_q = inicializa_tabla_q(lista_acciones, numero_filas, numero_columnas, destino)

    
    for episodio in range(numero_espisodios):
        estado_inicial= selecciona_estado_inicial(mapa, destino)
        accion_inicial= accion_max_recompensa(estado_inicial, tabla_q)
        
        
        while(estado_inicial != destino):
            print(estado_inicial, accion_inicial)
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
            print(estado_actual,accion_a_tomar)
            tabla_q[estado_inicial][accion_inicial] = tabla_q[estado_inicial][accion_inicial] + alpha*(recompensa+gamma*tabla_q[estado_actual][accion_a_tomar]-tabla_q[estado_inicial][accion_inicial])
            
            if not hay_colision(estado_actual, mapa):
                estado_inicial= estado_actual            
            accion_inicial= accion_a_tomar
        
        
        


mapa, destino = lee_mapa("mapa3.txt")   
lista_acciones = ['esperar','N','NE','E','SE','S','SO','O','NO']
indices_nav_acciones = {'esperar': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5, 'SO': 6, 'O': 7, 'NO': 8}
nav_estados = genera_estados(mapa)
nav_recompensas_sistema = crea_recompensas_sistema(nav_estados, lista_acciones, destino, mapa, 1000, 100)


aplica_SARSA(mapa, destino, lista_acciones, 1, nav_recompensas_sistema, indices_nav_acciones, 0.5, 0.9)