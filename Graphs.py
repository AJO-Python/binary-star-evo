# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:34:19 2019

@author: c1672922
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import orbit_functions as of
import Integrator
import matplotlib.colors as colors
import random

"""
Integrator.simulate("/home/josh/Documents/Binary_analysis",
                    False,
                    init_conds_directory = "/home/josh/Documents/Binary_analysis",
                    report_pos=100)

# %%
"""
run_name = "/run6"
run_dir = "/home/joshowen121/binary-star-evo/results"
direc = run_dir + run_name

"""
run_name = ""
run_dir = "/home/josh/Documents/Binary_analysis"
"""

#%%

x = of.get_single_data(run_dir + run_name + "/pos_x.csv")
y = of.get_single_data(run_dir + run_name + "/pos_y.csv")
z = of.get_single_data(run_dir + run_name + "/pos_z.csv")
init_vars = of.get_init_conds(direc + "/init_conds.txt")
N = int(init_vars[1])
N_cluster = int(init_vars[0])
colors_list = list(colors._colors_full_map.values())
plot_pos = 1


fig = plt.figure()
p1 = Axes3D(fig)
p1.set_xlim3d(0, 5e17)
p1.set_ylim3d(-1e16, 1e16)
p1.set_zlim3d(-1e16, 1e16)
for j in range(N_cluster):  # looping through cluster index
    col = random.choice(colors_list)
    for i in range(len(x[0])):  # looping through bodies index
        if i >= N*j and i < N*(j+1):
            #p1.plot(x[:-2:plot_pos, i], y[:-2:plot_pos, i], z[:-1:plot_pos, i], color=col)
            #p1.scatter(x[::plot_pos, i], y[::plot_pos, i], z[::plot_pos, i], color=col)
            #p1.scatter(x[-1, i], y[-1, i], z[-1, i], color=col)
            p1.scatter(x[0, i], y[0, i], z[0, i], color=col)
        else: pass

fig.show()
#fig = plt.savefig("positions.pdf")
