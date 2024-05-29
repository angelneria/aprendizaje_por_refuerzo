# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:56:21 2024

@author: manue
"""

from src.main.mapa import lee_mapa, visualiza_mapa




if __name__ == '__main__':  
    
    mapa,destino = lee_mapa("../../data/map.txt")
    print(mapa)
    print("")
    print(destino)


    visualiza_mapa(mapa, destino)