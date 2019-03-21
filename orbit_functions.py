
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:31:44 2018

@author: c1672922
"""
import numpy as np

G = 6.674e-11
au = 1.49597e11
pc = 3.0857e16
# =============================================================================
# Functions
# =============================================================================


def get_data_ready(filename):
    with open(filename) as f:
        ncols = len(f.readline().split(","))

    masses, rx, ry, rz, vx, vy, vz = np.genfromtxt(filename, delimiter=",",
                                                   usecols=range(1, ncols))
    masses, rx, ry, rz, vx, vy, vz = clean_data(masses, rx, ry, rz, vx, vy, vz)
    return masses, rx, ry, rz, vx, vy, vz


def clean_data(masses, rx, ry, rz, vx, vy, vz):
    masses = masses[4:]
    rx, ry, rz = rx[4:], ry[4:], rz[4:]
    vx, vy, vz = vx[4:], vy[4:], vz[4:]
    return masses, rx, ry, rz, vx, vy, vz


def get_single_data(filename):
    data = np.genfromtxt(filename, delimiter=",", unpack=True)
    return data


def save_interval(masses, pos_x, pos_y, pos_z, vx, vy, vz, dest, index):
    np.savetxt(dest+"/masses{}.csv".format(index), masses, delimiter=",")
    np.savetxt(dest+"/pos_x{}.csv".format(index), pos_x, delimiter=",")
    np.savetxt(dest+"/pos_y{}.csv".format(index), pos_y, delimiter=",")
    np.savetxt(dest+"/pos_z{}.csv".format(index), pos_z, delimiter=",")
    np.savetxt(dest+"/vel_x{}.csv".format(index), vx, delimiter=",")
    np.savetxt(dest+"/vel_y{}.csv".format(index), vy, delimiter=",")
    np.savetxt(dest+"/vel_z{}.csv".format(index), vz, delimiter=",")


def get_init_conds(filename):
    data = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            info = line.split("=")
            data.append(info[1])
    return data


def report_snapshot(time, Tmax, masses, vx, vy, vz, rx, ry, rz,
                    N, pos_x, pos_y, pos_z, eps):
    # Setting arrays
    momentum_body, kinetic_body, potential_body = [
            [] for _ in range(3)]
    # Getting the momentum and kinetic energy of each particle
    for i in range(N):
        speed = get_mag([vx[i], vy[i], vz[i]])
        momentum_body.append(get_momentum(speed, masses[i]))
        kinetic_body.append(get_kinetic(speed, masses[i]))
        # Storing the position data
        pos_x[i].append(rx[i])
        pos_y[i].append(ry[i])
        pos_z[i].append(rz[i])

        for j in range(N):
            if i == j:
                potential = 0
            else:
                potential = get_grav_potential(
                        masses[i], masses[j], (rx[i], ry[i], rz[i]),
                        (rx[j], ry[j], rz[j]))
            if (potential not in potential_body) or potential == 0:
                potential_body.append(potential)

    Ek, Ep, Mom = (
            sum(kinetic_body), sum(potential_body)*0.5, sum(momentum_body))
    return pos_x, pos_y, pos_z, Ek, Ep, Mom


def get_accel_soft(N, x, y, z, m, r_min, eps):
    mag_r_min = get_mag(r_min)
    ax = np.zeros(N)
    ay = np.zeros(N)
    az = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i == j:
                pass
            else:
                x_diff = x[i] - x[j]
                y_diff = y[i] - y[j]
                z_diff = z[i] - z[j]

                R = get_mag([x_diff, y_diff, z_diff])
                if R == 0:
                    raise ValueError("COLLISION")
                elif R < mag_r_min:
                    r_min = [x_diff, y_diff, z_diff]

                f = - (G*m[j]) / ((R**2 + eps**2)**(3/2))

                ax[i] += f * x_diff
                ay[i] += f * y_diff
                az[i] += f * z_diff
    return ax, ay, az, r_min


def get_momentum(v, m):
    # Gets momentum of an object
    return v*m


def get_mag(vector):
    # Gets magnitude of 3D vector
    return np.sqrt((vector[0]**2 + vector[1]**2 + vector[2]**2))


def get_kinetic(v, m):
    # Gets kinetic energy of object
    return 0.5 * m * (v**2)


def get_grav_potential(mass1, mass2, r1, r2):
    dist = np.subtract(r1, r2)
    return -G*mass1*mass2 / get_mag(dist)


def get_total_potential(N, masses, positions):
    potential = 0
    for i in range(N):
        for j in range(N):
            if i != j:
                potential += get_grav_potential(
                        masses[i], masses[j], positions[:, i], positions[:, j])
            else:
                potential += 0
    return potential


def get_com(position, mass):
    com_x = np.average(position[0], axis=0, weights=mass)
    com_y = np.average(position[1], axis=0, weights=mass)
    com_z = np.average(position[2], axis=0, weights=mass)
    com = np.array([com_x, com_y, com_z])
    return com


def adjust_pos(position, com):
    for i in range(0, len(position)):
        position[i] = np.subtract(position[i], com[i])
    return position


def get_completion(time, time_max, done):
    done_temp = done
    for i in range(10, -1, -1):
        if time > (time_max*i/10):
            if i not in done_temp:
                done_temp.append(i)
                # print("{} % completed".format(i*10))
                return done
    if done == done_temp:
        return done


def gen_masses(N):
    mass_sun = 1.989e30
    masses = np.random.normal(0.5*mass_sun, 0.02*mass_sun, N)
    return masses


def gen_xyz(N, spread):
    return np.random.normal(0, spread, (3, N))


def gen_cluster(N, mass_dist, pos_dist):
    masses = gen_masses(N)
    positions = gen_xyz(N, pos_dist*au)
    positions = adjust_pos(positions, get_com(positions, masses))
    pos_x = positions[0]
    pos_y = positions[1]
    pos_z = positions[2]
    init_vels = gen_xyz(N, 10e2)
    scaled_vels = np.array(scale_vels(masses, init_vels, positions, 2))
    group_vel = get_group_vel(masses, scaled_vels)
    final_vels = np.zeros((3, N))
    for i in range(3):
        for j in range(N):
            temp = np.subtract(scaled_vels[i, j], group_vel[i])
            final_vels[i, j] = temp
    cluster = np.array((masses, pos_x, pos_y, pos_z, final_vels[0],
                        final_vels[1], final_vels[2]))
    return cluster


def scale_vels(masses, init_vels, positions, virial):
    N = len(masses)
    kinetic = get_kinetic(get_mag(init_vels[:]), masses)
    kinetic_total = sum(kinetic)
    potential = -get_total_potential(N, masses, positions)
    x, y, z = init_vels[:]
    scaling_factor = potential/kinetic_total
    const = np.sqrt(scaling_factor / virial)
    x = x*const
    y = y*const
    z = z*const
    return x, y, z


def get_group_vel(masses, velocities):
    total_mass = sum(masses)
    x, y, z = 0, 0, 0
    for index, mass in enumerate(masses):
        x += velocities[0][index] * mass
        y += velocities[1][index] * mass
        z += velocities[2][index] * mass
    return x/total_mass, y/total_mass, z/total_mass


def gen_filament(Number_Clusters, Bodies_per_Cluster, mass_spread,
                 pos_spread, seed, prog_x, prog_y, prog_z):
    standard_progress = [prog_x, prog_y, prog_z]
    np.random.seed(seed)
    N = Bodies_per_Cluster
    prev_com = [0, 0, 0]
    cluster_list = np.empty((7, N))
    for i in range(Number_Clusters):
        progress = 0

        cluster = gen_cluster(N, mass_spread, pos_spread)
        x_pos = cluster[1]
        y_pos = cluster[2]
        z_pos = cluster[3]
        progress = np.add(filament_progression(
                        standard_progress[0], standard_progress[1],
                        standard_progress[2]), prev_com)

        x_pos = np.add(x_pos, progress[0])
        y_pos = np.add(y_pos, progress[1])
        z_pos = np.add(z_pos, progress[2])

        cluster_list = [np.append(cluster_list[0], cluster[0]),
                        np.append(cluster_list[1], x_pos),
                        np.append(cluster_list[2], y_pos),
                        np.append(cluster_list[3], z_pos),
                        np.append(cluster_list[4], cluster[4]),
                        np.append(cluster_list[5], cluster[5]),
                        np.append(cluster_list[6], cluster[6])]

        prev_com = get_com((x_pos, y_pos, z_pos), cluster[0])
    return cluster_list


def filament_progression(x, y, z):
    x_spread = np.random.randint((x-(x/10)), (x+(x/10)))
    y_spread = np.random.randint(-y/2, y/2)
    z_spread = np.random.randint(-z/2, z/2)
    result = np.array((x_spread, y_spread, z_spread))
    return result
