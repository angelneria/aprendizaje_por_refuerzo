# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:44:29 2024

@author: manue
"""
import mdptoolbox.mdp as mdp
import numpy as np
import matplotlib.pyplot as plt

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
    
    

def genera_estados(mapa):
    nav_estados = []
    for i in range(0,mapa.shape[1]):
        for j in range(0,mapa.shape[0]):
            nav_estados.append(tuple([i,j]))
    return nav_estados

def hay_colision(estado, mapa):
    return mapa[estado[1],estado[0]]==1


def obtiene_recompensa(estado, destino,mapa, K= 1000):
    if hay_colision(estado, mapa):
        valor = -K
  
    else:
        valor = - (abs(estado[0]-destino[0]) + abs(estado[1]-destino[1]))
    return valor


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
        



def visualiza_politica(politica, nav_estados, mapa, destino):
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


def obtiene_indice_estado(estado, mapa):
    return int(estado[0]*mapa.shape[0]+estado[1])


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


def crea_transiciones_movimiento(accion, prob_error, nav_estados, mapa):
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

    

            
