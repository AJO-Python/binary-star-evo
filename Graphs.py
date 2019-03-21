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


Integrator.simulate("/home/josh/Documents/Binary_analysis",
                    False,
                    init_conds_directory="/home/josh/Documents/Binary_analysis")


run_name=""
run_dir="/home/josh/Documents/Binary_analysis"



"""
run_name = "/run2"
run_dir = "/home/josh/Documents/results"
"""

x = of.get_single_data(run_dir + run_name + "/pos_x.csv")
y = of.get_single_data(run_dir + run_name + "/pos_x.csv")
z = of.get_single_data(run_dir + run_name + "/pos_x.csv")

plot_pos = 1
fig = plt.figure()
p1 = fig.add_subplot(111, projection="3d")
for i in range(len(x[0])):
    if i < 5: col = "r"
    elif i >= 5 and i < 10: col = "b"
    elif i >= 10 and i < 15: col = "g"
    elif i >= 15 and i < 20: col = "c"
    elif i >= 20 and i < 25: col = "k"
    elif i >= 25 and i < 30: col = "m"
    else: col = "y"
    p1.plot(x[::plot_pos, i], y[::plot_pos, i], z[::plot_pos, i], color=col)
    #p1.scatter(x[::plot_pos, i], y[::plot_pos, i], z[::plot_pos, i], color=col)
    p1.scatter(x[-1, i], y[-1, i], z[-1, i], color=col)
    p1.scatter(x[0, i], y[0, i], z[0, i], color="y")
fig.show()
fig = plt.savefig("positions.pdf")
