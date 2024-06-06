# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:26:30 2024

@author: Ángel
"""

from src.main.Montecarlo import *

if __name__ == '__main__':  
    mapa_grande,destino_grande = lee_mapa("../../data/map.txt")
    mapa_mediano, destino_mediano = lee_mapa("../../data/mapa2.txt")
    mapa_pequeño, destino_pequeño = lee_mapa("../../data/mapa3.txt")   
    
    lista_acciones = ['esperar','N','NE','E','SE','S','SO','O','NO']
    indices_nav_acciones = {'esperar': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5, 'SO': 6, 'O': 7, 'NO': 8}
    
    
    print("########################################### PRUEBA CON MAPA GRANDE ###########################################")
    print()
    
    print("Aplicando Montecarlo de primera visita al mapa grande con factor de descuento 0,9, K1=100, K2=1000 y 20 episodios")
    estado_inicial_grande=(2,4)
    nav_estados1 = genera_estados(mapa_grande)
    nav_recompensas_sistema_1 = crea_recompensas_sistema(nav_estados1, lista_acciones, destino_grande, mapa_grande, 1000, 100)
    aplica_Montecarlo(mapa_grande, destino_grande, lista_acciones, nav_estados1,estado_inicial_grande,20, 0.9, nav_recompensas_sistema_1, indices_nav_acciones, True)
    print("########################################### GRAFICO 1 GENERADO ###########################################")
    
    print("Aplicando Montecarlo de primera visita al mapa grande con factor de descuento 0,95, K1=100, K2=1000 y 35 episodios")
    estado_inicial_grande=(2,4)
    nav_estados1 = genera_estados(mapa_grande)
    nav_recompensas_sistema_1 = crea_recompensas_sistema(nav_estados1, lista_acciones, destino_grande, mapa_grande, 1000, 100)
    aplica_Montecarlo(mapa_grande, destino_grande, lista_acciones, nav_estados1,estado_inicial_grande,35, 0.95, nav_recompensas_sistema_1, indices_nav_acciones, True)
    print("########################################### GRAFICO 2 GENERADO ###########################################")
    
    print("Aplicando Montecarlo de cada visita al mapa grande con factor de descuento 0,9, K1=100, K2=1000 y 20 episodios")
    estado_inicial_grande=(2,4)
    nav_estados1 = genera_estados(mapa_grande)
    nav_recompensas_sistema_1 = crea_recompensas_sistema(nav_estados1, lista_acciones, destino_grande, mapa_grande, 1000, 100)
    aplica_Montecarlo(mapa_grande, destino_grande, lista_acciones, nav_estados1,estado_inicial_grande,20, 0.9, nav_recompensas_sistema_1, indices_nav_acciones)
    print("########################################### GRAFICO 3 GENERADO ###########################################")
    
    print("Aplicando Montecarlo de cada visita al mapa grande con factor de descuento 0,95, K1=100, K2=1000 y 35 episodios")
    estado_inicial_grande=(2,4)
    nav_estados1 = genera_estados(mapa_grande)
    nav_recompensas_sistema_1 = crea_recompensas_sistema(nav_estados1, lista_acciones, destino_grande, mapa_grande, 1000, 100)
    aplica_Montecarlo(mapa_grande, destino_grande, lista_acciones, nav_estados1,estado_inicial_grande,35, 0.95, nav_recompensas_sistema_1, indices_nav_acciones)
    print("########################################### GRAFICO 4 GENERADO ###########################################")
    
    print()
    print("########################################### PRUEBA CON MAPA MEDIANO ###########################################")
    print()
    
    print("Aplicando Montecarlo de primera visita al mapa mediano con factor de descuento 0,9, K1=100, K2=1000 y 30 episodios")
    estado_inicial_mediano=(2,6)
    nav_estados2 = genera_estados(mapa_mediano)
    nav_recompensas_sistema_2 = crea_recompensas_sistema(nav_estados2, lista_acciones, destino_mediano, mapa_mediano, 1000, 100)
    aplica_Montecarlo(mapa_mediano, destino_mediano, lista_acciones, nav_estados2,estado_inicial_mediano,30, 0.9, nav_recompensas_sistema_2, indices_nav_acciones, True)
    print("########################################### GRAFICO 5 GENERADO ###########################################")
    
    print("Aplicando Montecarlo de primera visita al mapa mediano con factor de descuento 0,95, K1=100, K2=1000 y 50 episodios")
    estado_inicial_mediano=(2,6)
    nav_estados2 = genera_estados(mapa_mediano)
    nav_recompensas_sistema_2 = crea_recompensas_sistema(nav_estados2, lista_acciones, destino_mediano, mapa_mediano, 1000, 100)
    aplica_Montecarlo(mapa_mediano, destino_mediano, lista_acciones, nav_estados2,estado_inicial_mediano,50, 0.95, nav_recompensas_sistema_2, indices_nav_acciones, True)
    print("########################################### GRAFICO 6 GENERADO ###########################################")
    
    
    print("Aplicando Montecarlo de cada visita al mapa mediano con factor de descuento 0,9, K1=100, K2=1000 y 30 episodios")
    estado_inicial_mediano=(2,6)
    nav_estados2 = genera_estados(mapa_mediano)
    nav_recompensas_sistema_2 = crea_recompensas_sistema(nav_estados2, lista_acciones, destino_mediano, mapa_mediano, 1000, 100)
    aplica_Montecarlo(mapa_mediano, destino_mediano, lista_acciones, nav_estados2,estado_inicial_mediano,30, 0.9, nav_recompensas_sistema_2, indices_nav_acciones)
    print("########################################### GRAFICO 7 GENERADO ###########################################")
    
     
    print("Aplicando Montecarlo de cada visita al mapa mediano con factor de descuento 0,95, K1=100, K2=1000 y 50 episodios")
    estado_inicial_mediano=(2,6)
    nav_estados2 = genera_estados(mapa_mediano)
    nav_recompensas_sistema_2 = crea_recompensas_sistema(nav_estados2, lista_acciones, destino_mediano, mapa_mediano, 1000, 100)
    aplica_Montecarlo(mapa_mediano, destino_mediano, lista_acciones, nav_estados2,estado_inicial_mediano,50, 0.95, nav_recompensas_sistema_2, indices_nav_acciones)
    print("########################################### GRAFICO 8 GENERADO ###########################################")
    
    print()
    print("########################################### PRUEBA CON MAPA PEQUEÑO ###########################################")
    print()
    
    print("Aplicando Montecarlo de primera visita al mapa pequeño con factor de descuento 0,9, K1=100, K2=1000 y 50 episodios")
    estado_inicial_pequeño=(7,1)
    nav_estados3 = genera_estados(mapa_pequeño)
    nav_recompensas_sistema_3 = crea_recompensas_sistema(nav_estados3, lista_acciones, destino_pequeño, mapa_pequeño, 1000, 100)
    aplica_Montecarlo(mapa_pequeño, destino_pequeño, lista_acciones, nav_estados3 ,estado_inicial_pequeño,50, 0.9, nav_recompensas_sistema_3, indices_nav_acciones, True)
    print("########################################### GRAFICO 9 GENERADO ###########################################")
    print()
    
    print("Aplicando Montecarlo de primera visita al mapa pequeño con factor de descuento 0,95, K1=100, K2=1000 y 75 episodios")
    estado_inicial_pequeño=(7,1)
    nav_estados3 = genera_estados(mapa_pequeño)
    nav_recompensas_sistema_3 = crea_recompensas_sistema(nav_estados3, lista_acciones, destino_pequeño, mapa_pequeño, 1000, 100)
    aplica_Montecarlo(mapa_pequeño, destino_pequeño, lista_acciones, nav_estados3 ,estado_inicial_pequeño,75, 0.95, nav_recompensas_sistema_3, indices_nav_acciones, True)
    print("########################################### GRAFICO 10 GENERADO ###########################################")
    print()
    
    print("Aplicando Montecarlo de cada visita al mapa pequeño con factor de descuento 0,9, K1=100, K2=1000 y 50 episodios")
    estado_inicial_pequeño=(7,1)
    nav_estados3 = genera_estados(mapa_pequeño)
    nav_recompensas_sistema_3 = crea_recompensas_sistema(nav_estados3, lista_acciones, destino_pequeño, mapa_pequeño, 1000, 100)
    aplica_Montecarlo(mapa_pequeño, destino_pequeño, lista_acciones, nav_estados3 ,estado_inicial_pequeño,50, 0.9, nav_recompensas_sistema_3, indices_nav_acciones)
    print("########################################### GRAFICO 11 GENERADO ###########################################")
    
    print("Aplicando Montecarlo de cada visita al mapa pequeño con factor de descuento 0,95, K1=100, K2=1000 y 75 episodios")
    estado_inicial_pequeño=(7,1)
    nav_estados3 = genera_estados(mapa_pequeño)
    nav_recompensas_sistema_3 = crea_recompensas_sistema(nav_estados3, lista_acciones, destino_pequeño, mapa_pequeño, 1000, 100)
    aplica_Montecarlo(mapa_pequeño, destino_pequeño, lista_acciones, nav_estados3 ,estado_inicial_pequeño,75, 0.95, nav_recompensas_sistema_3, indices_nav_acciones)
    print("########################################### GRAFICO 12 GENERADO ###########################################")


