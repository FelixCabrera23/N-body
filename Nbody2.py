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

###################################################
scale = 1000  # tamaño del sistema

kg = 10e23 # Dimensional de masa
m = 10e9 # Dimensional de distancia
s = 10 # Dimensional de tiempo
# Se ha prbado optimo con s = 10e4

Grafica = False # se generan graficas
dat = 1 # Cantidad de datos por paso

#####################################################

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
        U = U - (G*part[6]*p[6])/(r)

    return U

# Definimos la función de la energia cinetica
def Ek (part):
    """
    Esta función calcula la energia cinetica respecto del origen para una particula
    """

    k = (1/2)*part[6]*(part[2]**2+part[3]**2)

    return k

def L_p (part):
    """
    Esta función calcula el momentum angular de una particula dada respecto al origen
    """
    L = part[6]*(part[0]*part[3]-part[2]*part[1])

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

    ###############################################
    # Guardamos a un archivo los resultados
    file = open('posisiones.dat','w')

    for i in range(pasos):
        ########################################
        if Grafica:

            # Dibujamos las particulas
            fig = plt.figure()
            ax = fig.add_subplot()

            # Llenamos las listas U E, y ploteamos todas las particulas
            for p in sisn:

                ax.scatter(p[0],p[1])

            plt.axis([-scale,scale,-scale,scale])
            plt.show
        #############################################





        j = 0

        #copiamos la particula generando un nuevo sistema temporal
        sist = []
        Vn = []
        ang1 = []
        sist = sisn[:]

        # Variable de control momentum angular total

        Lto = 0

        # Este ciclo va a mover el sistema en sist y va a calcular las Vn y las va a guardar
        for j in range(len(sisn)):

            p = sisn[j] # Particula que vamos a tratar

            # Al inicio de cada ciclo guardamos con el formato de cada particula su posisción
            if (np.mod(i,dat)==0):
                file.write('%f      %f      ' % (p[0],p[1]))

            if (p[2] == 0 and p[3] != 0):
                ang11 = np.pi*0.5*(p[3]/abs(p[3]))
            elif (p[2]==0 and p[3] == 0):
                ang11 = 0
            else:
                ang11 = np.arctan(p[3]/p[2]) # Angulo original

            # Energias y momentum inicial
            Uo = U_pot(p,sis) # Energia potencial original
            Eo = Ek(p) # Energia cinetica original
            Lo = L_p(p) # Momentum angular original

            Lto = Lto + Lo

            # Ahora empezamos con los calculos de la nueva posición
            pn = sist[j]

            pn[0] = p[0] + p[2] + 0.5*p[4]
            pn[1] = p[1] + p[3] + 0.5*p[5]

            # Calculamos la magnitud de la velocidad en base a la energia inicial
            Uf = U_pot(pn,sist)  #Energia potencial en la nueva posición

            Vn1 = np.sqrt((2/pn[6])*(Uo+Eo-Uf))

            Vn.append(Vn1)
            ang1.append(ang11)

            # Calculamos la aceleracion
            ax = (Vn1*np.cos(ang11)-p[2])/s
            ay = (Vn1*np.sin(ang11)-p[3])/s

            # Movemos la particula de acuerdo a la velocidad anterior

            pn[4] = ax
            pn[5] = ay

        if (np.mod(i,dat)==0):
            file.write('\n')  # Salta el espacio entre datos guardados
        cond = True

        # Aqui empieza el proceso aleatorio, ira por todas las particulas y solo aceptara el paso hasta el final
        while cond:
            k = 0
            Ltf = 0
            for pn in sist:

                # Veamos la energia solamente
                ang2 = ang1[k] + (0.25*np.pi)*np.random.randn()
                # Empezamos moviendo la particula y asignandole la nueva velocidad

                vxn = Vn[k]*np.cos(ang2)
                vyn = Vn[k]*np.sin(ang2)

                pn[2] = vxn

                pn[3] = vyn

                Ln = L_p(pn)

                Ltf = Ltf + Ln

                k +=1

            # Calculando condición de aceptación

            if (Ltf == 0): continue

            dL = Lto/Ltf

            if (dL < 1.0001 and dL > 0.9999):
                cond = False
                l = 0
                for l in range(len(sisn)):
                    p = sisn[l]
                    pn = sist[l]
                    p[0] = pn[0]
                    p[1] = pn[1]
                    p[2] = pn[2]
                    p[3] = pn[3]
            else:
                continue


        # Mostramos la barra de abance
        progress(i,pasos, status = 'Calculando:')
    file.close()
    return sisn


# Sistema de ejemplo, dos particulas orbitando el centro de masa
# este sistema funciona mejor con s = 10e2
scale = 4
particulas.append([2,0,0,-0.1,0,0,1000])
particulas.append([-2,0,0,0.1,0,0,1000])
Montecarlo(particulas,300)

# Sistemas para comparar con el modelo de newton

# sistema de particulas orbitando el centro de masa
# scale = 800
# sistema7 = [[-400,0,0,0.12,0,0,80000000],[400,0,0,-0.12,0,0,80000000]]
# Montecarlo(sistema7,100000)

# Sistema sol tierra
# scale = 300
# sistema1 = [[0,0,0,0,0,0,19891000],[149.597870691,0,0,0.2978,0,0,59.7]]
# Montecarlo(sistema1,1000)
