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
Integrator.simulate("/home/josh/binary-star-evo/results/run5",
                    False,
                    init_conds_directory="/home/josh/binary-star-evo/results/run5",
                    report_pos=1)
"""
# %%

run_name = "/run6"
run_dir = "/home/josh/binary-star-evo/results"
direc = run_dir + run_name

"""
run_name = ""
run_dir = "/home/josh/Documents/Binary_analysis"
"""

#%%
x = of.get_single_data(run_dir + run_name + "/pos_x.csv")
y = of.get_single_data(run_dir + run_name + "/pos_y.csv")
z = of.get_single_data(run_dir + run_name + "/pos_z.csv")

max_length = min(len(x), len(y), len(z))
x, y, z = x[:max_length], y[:max_length], z[:max_length]
def min_max(array):
    current_min = 9e99
    current_max = -9e99
    for i in array:
        if min(i) < current_min:
            current_min = min(i)
        if max(i) > current_max:
            current_max = max(i)
    return current_min, current_max

init_vars = of.get_init_conds(direc + "/init_conds.txt")
N = int(init_vars[1])
N_cluster = int(init_vars[0])
"""
N = 5
N_cluster = 5
"""

colors_list = list(colors._colors_full_map.values())
plot_pos = 1

fig = plt.figure()
p1 = Axes3D(fig)
p1.set_xlim3d(min_max(x))
p1.set_ylim3d(min_max(y))
p1.set_zlim3d(min_max(z))
for j in range(N_cluster):  # looping through cluster index
    col = random.choice(colors_list)
    #for i in range(len(x[0])):  # looping through bodies index
    for i in range(8, 11):
        if i >= N*j and i < N*(j+1):
            p1.plot(x[::plot_pos, i], y[::plot_pos, i], z[::plot_pos, i], color=col)
            #p1.scatter(x[::plot_pos, i], y[::plot_pos, i], z[::plot_pos, i], color=col)
            p1.scatter(x[-1, i], y[-1, i], z[-1, i], color=col, marker=">")
            p1.scatter(x[0, i], y[0, i], z[0, i], color=col, marker="x")
        else: pass

fig.show()
#fig = plt.savefig("positions.pdf")
