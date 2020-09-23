#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:51:17 2020

@author: walberto

Solución al problema de N cuerpos por metodo momentum - energia
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import sys
from scipy import constants

# Definimos algunas constantes importantes
# Estas son las dimensionales con las que se trabajan

scale = 1000 # tamaño del sistema

kg = 10e23 # Dimensional de masa
m = 10e9 # Dimensional de distancia
s = 10e4 # Dimensional de tiempo

Go = constants.value("Newtonian constant of gravitation")

# Calculo de la constante nueva G

G = Go*((kg*(s**2))/(m**3))

random.seed(1999)
np.random.seed(1002)

# Primero calculamos la energia entre dos particulas
# las particulas las vamos a almacenar en una lista, lo que sera más facil de
# interpretar desde fortran.

particulas = [] # Este va a ser un array 
# particula [x,y,vx,vy,m]

# Cada particula tiene que conservar su energia "propia" esto es que la suma de 
# su energia potencial con su energia cinetica respecto al origen debe permanecer 
# Constante, suponemos que realiza el calculo de esta energias

# Definimos la función energia potencial
def U_pot (part,P_list):
    """
    Esta función calcula la energia potencial para una particula "part" en un 
    sistema descrito en la lista "P_list".
    """
    
    U = 0
    
    for p in P_list: 
        r = np.sqrt((part[0]-p[0])**2+(part[1]-p[1])**2)
        if r == 0:
            continue
        U = U - (G*part[4]*p[4])/(r)
        
    return U

# Definimos la función de la energia cinetica
def Ek (part):
    """
    Esta función calcula la energia cinetica respecto del origen para una particula
    """
    
    k = (1/2)*part[4]*(part[2]**2+part[3]**2)
    
    return k

def L_p (part):
    """
    Esta función calcula el momentum angular de una particula dada respecto al origen
    """
    
    L = part[4]*(part[0]*part[3]-part[2]*part[1])
    
    return L
    
    
####### Barra de abance
def progress(count, total, status=''):
    " Barra de progreso, ayuda a determinar el porcentaje del proceso"
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.flush()
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
        


# Aqui va a empezar el proceso de montecarlo

def Montecarlo (sis,pasos):
    """
    Este es el proceso de montecarlo 
    Siendo una funcion compleja se explicara por cada parte
    """
    
    # Parte 1, movimiento del sistema y calculo de la energia inicial
    # Primero hacemos una lista donde se van a almacenar las energias de las particulas
   
    sisn = sis[:] # sistema nuevo, a ser probado 
    
    for i in range(pasos):
        
        # Dibujamos las particulas
        fig = plt.figure()
        ax = fig.add_subplot()
        
        # Llenamos las listas U E, y ploteamos todas las particulas
        for p in sisn:         
            
            ax.scatter(p[0],p[1])
            
        plt.axis([-scale,scale,-scale,scale])
        plt.show
   
        # ahora tenemos que hacer montecarlo para nueva velocidades
        
        j = 0
        
        # Empieza el proceso aleatorio
        for j in range(len(sisn)):
            
            p = sisn[j]
                  
            Vo = np.sqrt(p[2]**2+p[3]**2) # Esta es la magnitud de la velocidad original
            if p[2] == 0:
                ang1 = np.pi*0.5*(p[3]/abs(p[3]))
            else:
                ang1 = np.arctan(p[3]/p[2]) # Angulo original
            Uo = U_pot(p,sis) # Energia potencial original
            Eo = Ek(p) # Energia cinetica original
            Lo = L_p(p) # Momentum angular original
            
            # En esta parte movemos aleatoriamente la particula
            # Emepezamos con distribuciones uniformes
            
            cond = True
            
            while cond:
                # Veamos la energia solamente
                sist = []
                sist = sisn[:]
                
                pn = sist[j]
                Vn = Vo + (Vo*0.25)*np.random.randn()                
                ang2 = ang1 + (0.5*np.pi)*np.random.randn()
                
                vxn = Vn*np.cos(ang2)
                vyn = Vn*np.sin(ang2)
                
                # Cono la nueva velocidad entonces ponemos las coordenadas de la nueva particula}
                
                pn[0] = p[0] + vxn
                
                pn[1] = p[1] + vyn
                
                pn[2] = vxn
                
                pn[3] = vyn
                
<<<<<<< HEAD
                Un = U_pot(pn,sist)
=======
                Un = U_pot(pn,sis) # sis no se ha movido, la particula se duplica
>>>>>>> 1bc271e197f163d2736c4102c8506b5aa1c643b9
                En = Ek(pn)
                Ln = L_p(pn)
                
                dU = (Eo+Uo+Lo)/(En+Un+Ln)
                
                if (dU < 1.1 and dU > 0.9):
                    cond = False
                    p[0] = pn[0]
                    p[1] = pn[1]
                    p[2] = pn[2]
                    p[3] = pn[3]
                else:
                    continue
            
                
        # Mostramos la barra de abance
        progress(i,pasos, status = 'Calculando:')

    return sisn






# Sistema de ejemplo, dos particulas estaticas en el eje x

particulas.append([2,0,0,0.1,1])
particulas.append([-2,0,0,-0.1,1])

# Montecarlo(particulas,100)

sistema7 = [[-400,0,0,5,800],[400,0,0,-5,800]]
Montecarlo(sistema7,1000)





