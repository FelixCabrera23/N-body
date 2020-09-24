#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:25:47 2020

@author: walberto

Graficas y animaciónes de Nbody2
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

"Esto lee los datos y los guarda en un array de numpy"
posiciones = np.loadtxt('posisiones.dat')

"Esto cambaia del array 3D a listas"
x,y,x1,y1 = zip(*posiciones)


scale = 1500

def configuracion ():

    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    ax1.set_xlim(-scale,scale)
    ax1.set_ylim(-scale,scale)

    l1 = ax1.plot(x,y,'-')
    l2 = ax1.plot(x1,y1,'-')

    plt.show()

configuracion()
