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
#random.seed(124)

# %%



def plot_graph(run_name,
               binary_to_plot=[],
               plot_pos=100,
               display="",
               x_dist=1e16,
               start=0):
    run_dir = "./results/"
    direc = run_dir + run_name
    x = of.get_single_data(direc + "/pos_x.csv")
    y = of.get_single_data(direc + "/pos_y.csv")
    z = of.get_single_data(direc + "/pos_z.csv")
    x, y, z = of.strip_trailing_data(x, y, z)

    init_vars = of.get_init_conds(direc + "/init_conds.txt")
    N = int(init_vars[1])
    N_cluster = int(init_vars[0])

    #colors_list = list(colors._colors_full_map.values())
    colors_list = list(["Blue", "Green", "Fuchsia", "black", "olive"])
    fig = plt.figure()
    p1 = Axes3D(fig)
    if display == "True":
        p1.set_xlim3d(0, x_dist)
        p1.set_ylim3d(-x_dist/2, x_dist/2)
        p1.set_zlim3d(-x_dist/2, x_dist/2)

    elif display == "All":
        p1.set_xlim3d(of.min_max(x))
        p1.set_ylim3d(of.min_max(y))
        p1.set_zlim3d(of.min_max(z))

    for j in range(N_cluster):  # looping through cluster index
        col = random.choice(colors_list)
        #col="blue"
        #for i, col in zip([4, 10, 13, 17], ["blue", "red", "red", "black"]):
        for i in range(len(x[0])):  # looping through bodies index
            if (i >= N*j and i < N*(j+1)) or (j==0 and i==0):
                if i in binary_to_plot:
                    p1.plot(x[::plot_pos, i],
                            y[::plot_pos, i],
                            z[::plot_pos, i],
                            color="red", linewidth=0.8)
                    p1.scatter(x[-1, i],
                               y[-1, i],
                               z[-1, i],
                               color="red", marker=">")
                    p1.scatter(x[0, i],
                               y[0, i],
                               z[0, i],
                               color="red", marker="o")
                else:
                    p1.plot(x[start::plot_pos, i],
                            y[start::plot_pos, i],
                            z[start::plot_pos, i],
                            color=col, linewidth=0.6, alpha=0.2)
                    p1.scatter(x[-1, i],
                               y[-1, i],
                               z[-1, i],
                               color=col, marker=">")
                    p1.scatter(x[0, i],
                               y[0, i],
                               z[0, i],
                               color=col, marker=".")
                    pass
            else:
                pass
    p1.set_xlabel("X (m)", linespacing=3.1)
    p1.set_ylabel("Y (m)", linespacing=3.1)
    p1.set_zlabel("Z (m)", linespacing=3.1)
    fig.show()
    # fig = plt.savefig("positions.pdf")
"""
plot_graph("3x4_standard_long", binary_to_plot=[1, 2],
           display="All",
           x_dist=2e16,
           plot_pos=1)
"""