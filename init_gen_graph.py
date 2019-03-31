#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:27:57 2019

@author: josh
"""
import os
import sys
import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import orbit_functions as of
import random


RUN_NAME = "test"


init_vars = of.get_init_conds("/home/josh/binary-star-evo/results/" + RUN_NAME + "/init_conds.txt")
init_vars = [int(i) for i in init_vars]
progression = list((init_vars[-3], init_vars[-2], init_vars[-1]))
init_vars = init_vars[0:-3]
# Generating initial_data
cluster_list = of.gen_filament(*init_vars, *progression)

# Saving init_conds to file
file_loc = "/home/josh/binary-star-evo/results/" + RUN_NAME + "/cluster.csv"
np.savetxt(file_loc, cluster_list, delimiter=",")
# Loading in data
masses, x, y, z, vx, vy, vz = of.get_data_ready(file_loc)
N = int(init_vars[1])
N_cluster = int(init_vars[0])

colors_list = list(colors._colors_full_map.values())
plot_pos = 1

fig = plt.figure()
p1 = Axes3D(fig)

#p1.set_xlim3d(of.min_max(x))
#p1.set_ylim3d(of.min_max(y))
#p1.set_zlim3d(of.min_max(z))

x_dist = 3e16

p1.set_xlim3d(0, x_dist)
p1.set_ylim3d(-x_dist/2, x_dist/2)
p1.set_zlim3d(-x_dist/2, x_dist/2)


for j in range(N_cluster):  # looping through cluster index
    col = random.choice(colors_list)
    #for i in [33, 34, 35, 36]:
    for i in range(len(x)):  # looping through bodies index
    #for i in range(6):
        if (i >= N*j and i < N*(j+1)) or (j==0 and i==0):
            p1.scatter(x[i], y[i], z[i], color=col, marker="x")
        else:
            pass

fig.show()
