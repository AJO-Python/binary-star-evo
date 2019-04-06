#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:27:57 2019

@author: josh

Used to check initial generation parameters
Uses "init_conds.txt" from folder "RUN_NAME"

"""
import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import orbit_functions as of
import random
np.random.seed(124)


RUN_NAME = "run2"
# Fetch initial conditions from txt file
init_vars = of.get_init_conds("./results/" + RUN_NAME + "/init_conds.txt")
# Format data to integer type
init_vars = [int(i) for i in init_vars]
# Formatting of XYZ cluster progression variable
progression = list((init_vars[-3], init_vars[-2], init_vars[-1]))
init_vars = init_vars[0:-3]

# Generating the filament
masses, x, y, z, vx, vy, vz = of.gen_filament(*init_vars, *progression)
N = int(init_vars[1])  # Number of bodies per cluster
N_cluster = int(init_vars[0])  # Number of clusters in filament

colors_list = list(colors._colors_full_map.values())
plot_pos = 1  # Data plotting interval. Set > 100 if graph is lagging

fig = plt.figure()
p1 = Axes3D(fig)

# Set axis to display data over the whole window
#p1.set_xlim3d(of.min_max(x))
#p1.set_ylim3d(of.min_max(y))
#p1.set_zlim3d(of.min_max(z))

# Set axis to display at 1:1:1 scale
x_dist = lamba x_max: _, x_max = of.min_max(x)  # Set to the x length of filament
p1.set_xlim3d(0, x_dist)
p1.set_ylim3d(-x_dist/2, x_dist/2)
p1.set_zlim3d(-x_dist/2, x_dist/2)


for j in range(N_cluster):  # looping through clusters to set same colour for whole cluster
    col = random.choice(colors_list)
    for i in range(len(x)):  # looping through bodies index
        if (i >= N*j and i < N*(j+1)) or (j==0 and i==0):  # Selecting only the bodies in the current cluster
            p1.scatter(x[i], y[i], z[i], color="col", marker="x")
p1.set_xlabel("X (m)", linespacing=3.1)
p1.set_ylabel("Y (m)", linespacing=3.1)
p1.set_zlabel("Z (m)", linespacing=3.1)
fig.show()
