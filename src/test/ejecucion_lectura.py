# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:56:21 2024

@author: manue
"""

from src.main import *

mapa,destino = lee_mapa("map.txt")
print(mapa)
print("")
print(destino)


visualiza_mapa(mapa, destino)