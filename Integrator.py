# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:43:24 2018

@author: c1672922
"""
import os
import time
import numpy as np
import orbit_functions as of
# =============================================================================
# Setting up system
# =============================================================================
# %%
G = 6.67408e-11
eps = 1e9
pc = 3.0857e16
au = 1.49597e11


def simulate(destination_directory,
             CONT_PREVIOUS=False,
             save_suffix="",
             init_conds_name="/init_conds.txt",
             init_conds_directory="",
             source_directory="",
             report_pos=100):
    """
    destination_directory = directory to save results to
    CONT_PREVIOUS = Continue from previous run (must be stored in destination_directory
    save_suffix = Use to save multiple runs in the same direcory (outdated - leave blank)
    init_conds_name = select the initial conditions file
    source_directory = location of files for continuing previous run - leave blank if same as destination_directory
    report_pos = Number of time steps between updating the save file
    """
    # Saving "init_conds.txt" to results directory
    source_cp = "cp " + init_conds_directory + init_conds_name
    os.popen(source_cp + " " + destination_directory + init_conds_name)

    if not CONT_PREVIOUS:
        # Generating the cluster from given initial conditions
        cluster_list = of.generate_full_filament(destination_directory,
                                                 init_conds_directory,
                                                 init_conds_name)
        num_to_strip = 0  # clean data by removing trailing points
        # Saving init_conds to file
        cluster_text = "/cluster.csv"
        file_loc = destination_directory + cluster_text
        np.savetxt(file_loc, cluster_list, delimiter=",")
        # Loading in data
        masses, rx, ry, rz, vx, vy, vz = of.get_data_ready(file_loc,
                                                           num_to_strip)
        N = len(masses)  # Getting number of bodies

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
    # Initialising variables/arrays
    dt = 10  # Time step
    t = 0
    Tmax=9.36e14
    count = 0
    eps = 1e9
    r_min = [1e50, 1e50, 1e50]  # Arbitrary value > minimum body seperation
    momentum, kinetic, potential, energy = [[] for _ in range(4)]
    pos_x, pos_y, pos_z = ([[] for _ in range(N)] for i in range(3))
    vel_x, vel_y, vel_z = ([[] for _ in range(N)] for i in range(3))
    r_array, dt_array, percent, time_count, time_to_run, sim_time = [[] for _ in range(6)]
    ax, ay, az, r_min = of.get_accel_soft(N, rx, ry, rz, masses, r_min, eps)

    # Starting main loop and timer
    start = time.time()
    while t <= Tmax:  # Loop until close program\
        # Using a_0 to calculate vel(t + dt/2) and pos(t + dt/2)
        vx[:] += 0.5*(ax[:])*dt
        vy[:] += 0.5*(ay[:])*dt
        vz[:] += 0.5*(az[:])*dt
        # pos(t + dt)
        rx[:] += vx[:]*dt
        ry[:] += vy[:]*dt
        rz[:] += vz[:]*dt
        # Update acceleration to a(t + dt)
        ax, ay, az, r_temp = of.get_accel_soft(
                N, rx, ry, rz, masses, r_min, eps)
        # Scaling the softening paramter
        #eps_temp = of.get_mag(r_temp)
        #eps = eps_temp if eps_temp > 1e9 else 1e9
        # Calculating v(t + dt)
        vx[:] += 0.5*(ax[:])*dt
        vy[:] += 0.5*(ay[:])*dt
        vz[:] += 0.5*(az[:])*dt

        # Save data to file at certain intervals
        if count % report_pos == 0:
            pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, Ek, Ep, Mom = (
                    of.report_snapshot(t, Tmax, masses, vx, vy, vz,
                                       rx, ry, rz, N,
                                       pos_x, pos_y, pos_z,
                                       vel_x, vel_y, vel_z, eps))
            # To get percentage displayed:
            # -> uncomment the print line of of.get_completion()
            # -> Set a Tmax outside of loop
            percent = of.get_completion(t, Tmax, percent)
            Et = Ek + Ep
            kinetic.append(Ek)
            potential.append(Ep)
            momentum.append(Mom)
            energy.append(Et)
            of.save_interval(masses, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z,
                             destination_directory, index=save_suffix)
            np.savetxt(destination_directory+"/run_time.csv", time_to_run)
            np.savetxt(destination_directory+"/sim_time.csv", sim_time)
            np.savetxt(destination_directory+"/time_step.csv", dt_array)
            np.savetxt(destination_directory+"/kinetic.csv", kinetic)
            np.savetxt(destination_directory+"/potential.csv", potential)
            end = time.time()
            time_to_run.append(end-start)
            sim_time.append(t)
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
