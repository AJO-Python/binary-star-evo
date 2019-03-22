# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:43:24 2018

@author: c1672922
"""

import orbit_functions as of
import numpy as np
import time
import os

# =============================================================================
# Setting up system
# =============================================================================
# %%
G = 6.67408e-11
eps = 5e6
pc = 3.0857e16
au = 1.49597e11

#if __name__ == __main__:
#    simulate("/home/ug/c1672922/code", False)


def simulate(destination_directory, CONT_PREVIOUS,
             save_suffix="",
             init_conds_name="/init_conds.txt",
             init_conds_directory="/home/ug/c1672922/code",
             source_directory="",
             report_pos=100):
    source_cp = "cp " + init_conds_directory + init_conds_name
    os.popen(source_cp + " " + destination_directory + init_conds_name)

    if not CONT_PREVIOUS:
        # Getting init_conds for simulation
        # Formatting of data
        of.clean_results_files(destination_directory)
        init_vars = of.get_init_conds(init_conds_directory + init_conds_name)
        init_vars = [int(i) for i in init_vars]
        progression = list((init_vars[-3], init_vars[-2], init_vars[-1]))
        init_vars = init_vars[0:-3]
        num_to_strip=0
        #num_to_strip = init_vars[1]-1
        # Generating initial_data
        cluster_list = of.gen_filament(*init_vars, *progression)
        # Saving init_conds to file
        cluster_text = "/cluster.csv"
        file_loc = destination_directory + cluster_text
        np.savetxt(file_loc, cluster_list, delimiter=",")
        # Loading in data
        masses, rx, ry, rz, vx, vy, vz = of.get_data_ready(file_loc,
                                                           num_to_strip)
        N = len(masses)

    elif CONT_PREVIOUS:
        masses = of.get_single_data(source_directory+"/masses.csv")
        rx = of.get_single_data(source_directory+"/pos_x.csv")
        ry = of.get_single_data(source_directory+"/pos_y.csv")
        rz = of.get_single_data(source_directory+"/pos_z.csv")
        vx = of.get_single_data(source_directory+"/vel_x.csv")
        vy = of.get_single_data(source_directory+"/vel_y.csv")
        vz = of.get_single_data(source_directory+"/vel_z.csv")
        N = len(masses)

    # =============================================================================
    # Main body
    # =============================================================================
    # %%
    Tmax = 3.3e9  # Total integration time
    dt = 10  # Time step
    time_count = []
    t = 0
    count = 0
    r_min = [1e50, 1e50, 1e50]
    r_array = []
    momentum, kinetic, potential, energy = [[] for _ in range(4)]
    pos_x, pos_y, pos_z = ([[] for _ in range(N)] for i in range(3))
    percent = []
    ax, ay, az, r_min = of.get_accel_soft(N, rx, ry, rz, masses, r_min, eps)
    dt_array = []
    time_to_run = []
    sim_time = []
    start = time.time()
    while count >= 0:  # Iterating through by dt to Tmax
        # Using a_0 to calculate vel(t + dt/2) and pos(t + dt/2)
        vx[:] += 0.5*(ax[:])*dt
        vy[:] += 0.5*(ay[:])*dt
        vz[:] += 0.5*(az[:])*dt
        # pos(t + dt)
        rx[:] += vx[:]*dt
        ry[:] += vy[:]*dt
        rz[:] += vz[:]*dt
        # Update acceleration to (t + dt)
        ax, ay, az, r_temp = of.get_accel_soft(
                N, rx, ry, rz, masses, r_min, eps)
        # eps = of.get_mag(r_temp) / 64
        # Calculating v(t + dt)
        vx[:] += 0.5*(ax[:])*dt
        vy[:] += 0.5*(ay[:])*dt
        vz[:] += 0.5*(az[:])*dt

        # Every x time steps the position is added to an array for plotting
        if count % report_pos == 0:
            pos_x, pos_y, pos_z, Ek, Ep, Mom = (
                    of.report_snapshot(t, Tmax, masses, vx, vy, vz,
                                       rx, ry, rz, N,
                                       pos_x, pos_y, pos_z, eps))
            percent = of.get_completion(t, Tmax, percent)
            Et = Ek + Ep
            kinetic.append(Ek)
            potential.append(Ep)
            momentum.append(Mom)
            energy.append(Et)
            of.save_interval(masses, pos_x, pos_y, pos_z, vx, vy, vz,
                             destination_directory, index=save_suffix)
            end = time.time()
            time_to_run.append(end-start)
            sim_time.append(t)
            np.savetxt(destination_directory+"/run_time.csv", time_to_run)
            np.savetxt(destination_directory+"/sim_time.csv", sim_time)
        # Closest approach calculations and storing
        R_min = of.get_mag(r_min)
        R_temp = of.get_mag(r_temp)
        if R_temp < R_min:
            r_min = r_temp
            R_min = of.get_mag(r_min)
        r_array.append(R_min)

        # Dynamic time step calculation
        a = of.get_mag([ax, ay, az])
        dt = np.sqrt(2*0.66*eps/max(a))
        dt_array.append(dt)
        # eps = (3/4)*max(a)*dt**2
        # Incrementing relevant counters
        time_count.append(t)
        t += dt
        count += 1
