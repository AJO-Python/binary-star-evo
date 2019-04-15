#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 21:27:21 2019

@author: josh
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import orbit_functions as of
import Integrator
import random


def make_gif(run_name,
               num_frames,
               binary_to_plot=[],
               plot_pos=1,
               display="",
               x_dist=1e16,
               start=0,
               save_dir=""):
    run_dir = "./results/"
    direc = run_dir + run_name
    global x
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
    p1.view_init(elev= 28, azim = -65)
    #p1.dist=4
    plt.ioff()
    if display == "True":
        p1.set_xlim3d(0, x_dist)
        p1.set_ylim3d(-x_dist/2, x_dist/2)
        p1.set_zlim3d(-x_dist/2, x_dist/2)

    elif display == "All":
        p1.set_xlim3d(of.min_max(x))
        p1.set_ylim3d(of.min_max(y))
        p1.set_zlim3d(of.min_max(z))

    elif display == "Custom":
        p1.set_xlim3d(0e16, 2e16)
        p1.set_ylim3d(-0.5e16, 1.5e16)
        p1.set_zlim3d(-0.5e16, 1e16)

    # Selecting frames
    num_points = len(x)
    frame_freq = int(num_points/num_frames)
    frames = [frame_freq*index for index in range(num_frames)]
    for frame in frames:
        for j in range(N_cluster):  # looping through cluster index
            #col = random.choice(colors_list)
            col="blue"
            #for i, col in zip([4, 10, 13, 17], ["blue", "red", "red", "black"]):
            for i in range(len(x[0])):  # looping through bodies index
                if (i >= N*j and i < N*(j+1)) or (j==0 and i==0):
                    if frame < frame_freq:
                        if i in binary_to_plot:
                            p1.plot(x[:frame, i], y[:frame, i], z[:frame, i], color="red", linewidth=0.8)
                        else:
                            p1.plot(x[:frame, i], y[:frame, i], z[:frame, i], color=col, linewidth=0.5, alpha=0.5)
                    else:
                        if i in binary_to_plot:
                            p1.plot(x[(frame-frame_freq):frame, i], y[(frame-frame_freq):frame, i], z[(frame-frame_freq):frame, i], color="red", linewidth=0.8)
                            #p1.scatter(x[0, i], y[0, i], z[0, i], color="red", marker="x")
                        else:
                            p1.plot(x[(frame-frame_freq):frame, i], y[(frame-frame_freq):frame, i], z[(frame-frame_freq):frame, i], color=col, linewidth=0.5, alpha=0.5)
                            #p1.scatter(x[frame, i], y[frame, i], z[frame, i], color=col, marker=".")
                else:
                    pass
        fig = plt.savefig(f"./{save_dir}{run_name}{frame}.png")
        print(f"Frame number {int(frame/frame_freq)}/{num_frames}...")
        #plt.show()


make_gif("present_data",
         num_frames=100,
         binary_to_plot=[7, 10, 13, 4],
         display="Custom",
         save_dir="runs-to-save/gif_test_4/")