# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:56:21 2024

@author: manue
"""
import mdptoolbox.mdp as mdp
from src.main.mapa import lee_mapa, visualiza_mapa




if __name__ == '__main__':  
    nav_acciones = ['esperar','N','NE','E','SE','S','SO','O','NO']
    indices_nav_acciones = {'esperar': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5, 'SO': 6, 'O': 7, 'NO': 8}
    
    mapa,destino = lee_mapa("../../data/map.txt")
    print(mapa)
    print("")
    print(destino)


    visualiza_mapa(mapa, destino)