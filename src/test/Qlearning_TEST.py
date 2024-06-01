# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:56:21 2024

@author: manue
"""
import mdptoolbox.mdp as mdp
from src.main.Qlearning import *




if __name__ == '__main__':  
    mapa_grande,destino_grande = lee_mapa("../../data/map.txt")
    mapa_mediano, destino_mediano = lee_mapa("../../data/mapa2.txt")
    mapa_pequeño, destino_pequeño = lee_mapa("../../data/mapa3.txt")
    nav_acciones = ['esperar','N','NE','E','SE','S','SO','O','NO']
    indices_nav_acciones = {'esperar': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5, 'SO': 6, 'O': 7, 'NO': 8}
    nav_estados = genera_estados(mapa_grande)
    nav_estados2 = genera_estados(mapa_mediano)
    nav_estados3 = genera_estados(mapa_pequeño)
    
    

    
    print("Aplicando Q-learning al mapa grande con factor de descuento 0,9 y porcentaje de error total del 20% y 200000 iteraciones")
    nav_transiciones_sistema = crea_transiciones_sistema(0.2, nav_estados, mapa_grande)
    nav_recompensas_sistema = crea_recompensas_sistema(nav_estados, nav_acciones, destino_grande, mapa_grande, 1000, 100)
    aplica_Qlearning(0.9,nav_transiciones_sistema, nav_recompensas_sistema, nav_acciones, nav_estados, mapa_grande, destino_grande, 200000)
    print("########################################### GRAFICO 1 GENERADO ###########################################")
    

    print("Aplicando Q-learning al mapa mediano con factor de descuento 0,9 y porcentaje de error total del 20% y 200000 iteraciones")
    nav_transiciones_sistema2 = crea_transiciones_sistema(0.2, nav_estados2, mapa_mediano)
    nav_recompensas_sistema2 = crea_recompensas_sistema(nav_estados2, nav_acciones, destino_mediano, mapa_mediano, 1000, 100)
    aplica_Qlearning(0.9,nav_transiciones_sistema2, nav_recompensas_sistema2, nav_acciones, nav_estados2, mapa_mediano, destino_mediano, 200000)
    print("########################################### GRAFICO 2 GENERADO ###########################################")
    

    print("Aplicando Q-learning al mapa pequeño con factor de descuento 0,9 y porcentaje de error total del 20% y 200000 iteraciones")
    nav_transiciones_sistema3 = crea_transiciones_sistema(0.2, nav_estados3, mapa_pequeño)
    nav_recompensas_sistema3 = crea_recompensas_sistema(nav_estados3, nav_acciones, destino_pequeño, mapa_pequeño, 1000, 100)
    aplica_Qlearning(0.9,nav_transiciones_sistema3, nav_recompensas_sistema3, nav_acciones, nav_estados3, mapa_pequeño, destino_pequeño, 200000)
    print("########################################### GRAFICO 3 GENERADO ###########################################")

    
    