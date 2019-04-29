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


def get_moving_average(interval, window_size):
    window= np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def plot_graph(run_name,
               binary_to_plot=[],
               plot_pos=100,
               display="",
               x_dist=1e16,
               start=0,
               run_dir="./results/"):
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
                            color="blue", linewidth=0.8)
                    p1.scatter(x[-1, i],
                               y[-1, i],
                               z[-1, i],
                               color=col, marker=">")
                    p1.scatter(x[0, i],
                               y[0, i],
                               z[0, i],
                               color="red", marker="x")
                    p1.text(x[-1, i], y[-1, i], z[-1, i], "{}".format(i))
                else:
                    p1.plot(x[start::plot_pos, i],
                            y[start::plot_pos, i],
                            z[start::plot_pos, i],
                            color=col, linewidth=0.6, alpha=0.5)
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
    #p1.set_xlim3d(1e15, 6e15)
    #p1.set_ylim3d(-1, 4e15)
    #p1.set_zlim3d(0, 5e15)
    p1.set_xlabel("X (m)", linespacing=3.1)
    p1.set_ylabel("Y (m)", linespacing=3.1)
    p1.set_zlabel("Z (m)", linespacing=3.1)
    fig.show()
    # fig = plt.savefig("positions.pdf")

def plot_secondary_graphs(run_name,
                          run_dir="./results/",
                          plot_pos=100,
                          to_plot=["energy"]):
    direc = run_dir + run_name
    data_to_fetch = ["/time_step.csv", "/sim_time.csv", "/run_time.csv",
                     "/potential.csv", "/kinetic.csv"]
    data = [of.get_single_data(direc + x) for x in data_to_fetch]
    data_len = len(data[0])
    for i in range(1, 5):
        temp_len = len(data[i])
        if temp_len < data_len:
            data_len = temp_len
        for i in range(1, 5):
            data[i] = data[i][:data_len]
    total_energy = data[3]-data[4]
    total_energy_av = get_moving_average(total_energy, 100)
    dt = data[0]
    start=0
    end=-1
    
    if "energy" in to_plot:
        plt.figure()
        plt.plot(data[1][start:end],
                 data[3][start:end], label="Potential Energy")
        plt.plot(data[1][start:end],
                 data[4][start:end], label="Kinetic Energy")
        plt.plot(data[1][start:end],
                 total_energy_av[start:end], label="Total Energy")
        plt.xlabel("Simulation time (s)")
        plt.ylabel("Energy (J)")
        plt.title("{}: Energy of system".format(run_name))
        plt.legend(loc="best")
        slope, intercept = np.polyfit(total_energy_av,
                                      np.arange(len(total_energy)), 1)
        plt.annotate("Gradient of total energy:\n{:.3e}".format(slope),
                     xy=(0.6, 0.3),
                     xycoords='axes fraction')
        plt.grid()
        plt.savefig("results/graphs/{a}energy.png".format(a=run_name))

    if "time" in to_plot:
        fig = plt.figure()
        ax = fig.add_subplot(211)
        ax.set_title("{}: Time step per calculation".format(run_name))
        ax.semilogy(data[0], label="Time step")
        ax.legend(loc="best")
        ax.set_xlabel("Calculation number")
        ax.set_ylabel("Time step (s)")
        ax.grid()

        ax2 = fig.add_subplot(212)
        ax2.set_title("{}: Time step per calculation (last 5000 points)".format(run_name))
        ax2.semilogy(data[0][-5000:], label="Time step")
        ax2.legend(loc="lower right")
        ax2.set_xlabel("Calculation number")
        ax2.set_ylabel("Time step (s)")
        ax2.grid()
        plt.tight_layout(pad=0.4, h_pad=1)
        plt.savefig("results/graphs/{a}time.png".format(a=run_name))

    if "sim_run" in to_plot:
        plt.figure()
        plt.loglog(data[2], data[1])
        plt.xlabel("Run time (s)")
        plt.ylabel("Simulation time (s)")
        plt.title("{}: Run time against simulation time".format(run_name))
        plt.grid()
        plt.savefig("results/graphs/{a}sim_run.png".format(a=run_name))
    return data, dt

runs = ["1x5_standard",
        "3x3_standard", "5x3_standard", "6x3_standard",
        "3x5_standard", "4x3_standard"]
for run in runs:
    data, dt = plot_secondary_graphs(run, to_plot=["energy"])

"""
plot_graph("6x3_standard",
           display="True",
           x_dist=2e16,
           binary_to_plot=[],
           plot_pos=100)
"""
"""
plot_graph("3x4_standard_long", binary_to_plot=[1, 2],
           display="All",
           x_dist=2e16,
           plot_pos=1)
"""