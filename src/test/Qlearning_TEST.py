# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:56:21 2024

@author: manue
"""
import mdptoolbox.mdp as mdp
from src.main.Qlearning import *




if __name__ == '__main__':  
    mapa,destino = lee_mapa("../../data/map.txt")
    nav_acciones = ['esperar','N','NE','E','SE','S','SO','O','NO']
    indices_nav_acciones = {'esperar': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5, 'SO': 6, 'O': 7, 'NO': 8}
    nav_estados = genera_estados(mapa)



    visualiza_mapa(mapa, destino)
    
    
    nav_transiciones_sistema = crea_transiciones_sistema(0.1, nav_estados, mapa)
    nav_recompensas_sistema = crea_recompensas_sistema(nav_estados, nav_acciones, destino, mapa)
    
    aplica_Qlearning(0.9,nav_transiciones_sistema, nav_recompensas_sistema, nav_acciones, nav_estados, mapa, destino)