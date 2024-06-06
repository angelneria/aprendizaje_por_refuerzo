# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:33:13 2024

@author: Ángel
"""

from src.main.SARSA import *

if __name__ == '__main__':  
    mapa_grande,destino_grande = lee_mapa("../../data/map.txt")
    mapa_mediano, destino_mediano = lee_mapa("../../data/mapa2.txt")
    mapa_pequeño, destino_pequeño = lee_mapa("../../data/mapa3.txt")   
    
    lista_acciones = ['esperar','N','NE','E','SE','S','SO','O','NO']
    indices_nav_acciones = {'esperar': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5, 'SO': 6, 'O': 7, 'NO': 8}
    
    
    print("########################################### PRUEBA CON MAPA GRANDE ###########################################")
    print()
    
    print("Aplicando SARSA al mapa grande con α=0.5, γ=0,9 , K1=100, K2=1000 y 10000 episodios")
    nav_estados1 = genera_estados(mapa_grande)
    nav_recompensas_sistema_1 = crea_recompensas_sistema(nav_estados1, lista_acciones, destino_grande, mapa_grande, 1000, 100)
    aplica_SARSA(mapa_grande, destino_grande, lista_acciones, nav_estados1,10000,nav_recompensas_sistema_1, indices_nav_acciones, 0.5, 0.9)
    print("########################################### GRAFICO 1 GENERADO ###########################################")
    
    print("Aplicando SARSA al mapa grande con α=0.1, γ=0,87 , K1=100, K2=1000 y 10000 episodios")
    nav_estados1 = genera_estados(mapa_grande)
    nav_recompensas_sistema_1 = crea_recompensas_sistema(nav_estados1, lista_acciones, destino_grande, mapa_grande, 1000, 100)
    aplica_SARSA(mapa_grande, destino_grande, lista_acciones, nav_estados1,10000,nav_recompensas_sistema_1, indices_nav_acciones, 0.1, 0.87)
    print("########################################### GRAFICO 2 GENERADO ###########################################")
    
    print()
    print("########################################### PRUEBA CON MAPA MEDIANO ###########################################")
    print()
    
    print("Aplicando SARSA al mapa mediano con α=0.5, γ=0,9 , K1=100, K2=1000 y 10000 episodios")
    nav_estados2 = genera_estados(mapa_mediano)
    nav_recompensas_sistema_2 = crea_recompensas_sistema(nav_estados2, lista_acciones, destino_mediano, mapa_mediano, 1000, 100)
    aplica_SARSA(mapa_mediano, destino_mediano, lista_acciones, nav_estados2,10000,nav_recompensas_sistema_2, indices_nav_acciones, 0.5, 0.9)
    print("########################################### GRAFICO 3 GENERADO ###########################################")
    
    print("Aplicando SARSA al mapa mediano con α=0.1, γ=0,87 , K1=100, K2=1000 y 10000 episodios")
    nav_estados2 = genera_estados(mapa_mediano)
    nav_recompensas_sistema_2 = crea_recompensas_sistema(nav_estados2, lista_acciones, destino_mediano, mapa_mediano, 1000, 100)
    aplica_SARSA(mapa_mediano, destino_mediano, lista_acciones, nav_estados2,10000,nav_recompensas_sistema_2, indices_nav_acciones, 0.1, 0.87)
    print("########################################### GRAFICO 4 GENERADO ###########################################")
    
    print()
    print("########################################### PRUEBA CON MAPA PEQUEÑO ###########################################")
    print()
    
    print("Aplicando SARSA al mapa pequeño con α=0.5, γ=0,9 , K1=100, K2=1000 y 10000 episodios")
    nav_estados3 = genera_estados(mapa_pequeño)
    nav_recompensas_sistema_3 = crea_recompensas_sistema(nav_estados3, lista_acciones, destino_pequeño, mapa_pequeño, 1000, 100)
    aplica_SARSA(mapa_pequeño, destino_pequeño, lista_acciones, nav_estados3,10000,nav_recompensas_sistema_3, indices_nav_acciones, 0.5, 0.9)
    print("########################################### GRAFICO 5 GENERADO ###########################################")
    
    print("Aplicando SARSA al mapa pequeño con α=0.1, γ=0,87 , K1=100, K2=1000 y 10000 episodios")
    nav_estados3 = genera_estados(mapa_pequeño)
    nav_recompensas_sistema_3 = crea_recompensas_sistema(nav_estados3, lista_acciones, destino_pequeño, mapa_pequeño, 1000, 100)
    aplica_SARSA(mapa_pequeño, destino_pequeño, lista_acciones, nav_estados3,10000,nav_recompensas_sistema_3, indices_nav_acciones, 0.1, 0.87)
    print("########################################### GRAFICO 6 GENERADO ###########################################")
    
    