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

"""
Integrator.simulate("/home/josh/Documents/Binary_analysis",
                    False,
                    init_conds_directory = "/home/josh/Documents/Binary_analysis",
                    report_pos=100)

# %%
"""
run_name = "/run4"
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

plot_pos = 1
fig = plt.figure()
#p1 = fig.add_subplot(111, projection="3d")
p1 = Axes3D(fig)
#p1.set_xlim3d(0, 2e15)
#p1.set_ylim3d(-1e15, 1e15)
#p1.set_zlim3d(-1e15, 1e15)
for i in range(len(x[0])):
    if i < 5: col = "r"
    elif i >= 5 and i < 10: col = "b"
    elif i >= 10 and i < 15: col = "g"
    elif i >= 15 and i < 20: col = "c"
    elif i >= 20 and i < 25: col = "k"
    elif i >= 25 and i < 30: col = "m"
    else: col = "y"
    p1.plot(x[:-2:plot_pos, i], y[:-2:plot_pos, i], z[:-1:plot_pos, i], color=col)
    #p1.scatter(x[::plot_pos, i], y[::plot_pos, i], z[::plot_pos, i], color=col)
    p1.scatter(x[-1, i], y[-1, i], z[-1, i], color=col)
    p1.scatter(x[0, i], y[0, i], z[0, i], color=col, marker="o")
fig.show()
#fig = plt.savefig("positions.pdf")
