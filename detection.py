#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:10:24 2019

@author: josh
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import orbit_functions as of
import Graphs as gr
np.random.seed(124)

G = 6.674e-11
au = 1.49597e11
pc = 3.0857e16

"""
TODO:


"""


class body_class:
    # Class count of how many bodies have been created
    # and what the unique ID counter and total system mass are
    num_bodies = 0
    ID = 0
    total_mass = 0

    def __init__(self, mass, position, velocity, order=1, base=""):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.order = order
        self.ID = body_class.ID  # Assigning unique ID
        # Checking if the star is a single or multiple already
        if self.order == 1:
            self.base = str(self.ID)  # setting the base to the ID if single
        else:
            self.base = base
            # Setting base to the passed in argument
            # of "base". This is the IDs of the base objects
        # Mainting the class counters
        body_class.num_bodies += 1
        body_class.ID += 1
        body_class.total_mass += mass

    def show_atts(self):
        # Used to print all attributes of a body
        print("ID: ", self.ID)
        print("Order: ", self.order)
        print("Base: ", self.base)
        print("Mass: ", self.mass)
        print("Position: ", self.position)
        print("Velocity: ", self.velocity)
        print()


class binary:
    # Describes a system comprised of two bodies
    num_binaries = 0

    def __init__(self, binary_ID):  # Initialise with combined binary body ID
        global binary_index  # Pass in the global body arrrays
        global body_list
        ID_str, potential = binary_index[binary_ID]
        body1_ID, body2_ID = ID_str[0].split("-")
        body1, body2 = body_list[int(body1_ID)], body_list[int(body2_ID)]
        # Setting primary and secondary bodies by mass
        self.primary = body1 if body1.mass >= body2.mass else body2
        self.secondary = body1 if self.primary != body1 else body2
        # Setting binary paramters
        self.ID = binary.num_binaries
        #self.mass, self.com, self.vel, self.order = merge(body1, body2)
        # Effective mass for force calculations
        self.emass = get_eff_mass(body1.mass, body2.mass)
        self.EK = get_binary_kinetic(body1, body2)
        self.EP = potential
        # Semi-major axis (sma)
        self.sma = -(G*body1.mass*body2.mass) / (2*(self.EK + self.EP))
        # Mass ratio
        self.mr = self.primary.mass / self.secondary.mass
        self.base = [self.primary.ID, self.secondary.ID]
        #self.period = get_binary_period()


def get_binary_kinetic(body1, body2):
    #body1.show_atts()
    v1 = of.get_mag(body1.velocity)
    v2 = of.get_mag(body2.velocity)
    EK_1 = of.get_kinetic(v1, body1.mass)
    EK_2 = of.get_kinetic(v2, body2.mass)
    #print ("EK_1, EK_2: ", EK_1, EK_2)
    return EK_1 + EK_2


#def get_binary_period():
def get_eff_mass(m1, m2):
    return (m1*m2)/(m1+m2)


def detect_binaries(run_name, calc_index):  # e.g "results2.py"
    body_list = create_body_objects("./results/" + run_name, calc_index)
    all_bodies = [body for body in body_list]
    global binary_index
    binary_index = {}
    highest_order = 0
    counter = 0

    while len(body_list) > 1:  # Recalculating after every binary is found
        binary_body = None  # Clearing the variable

        # Getting the most bound binary and the indexes of the bodies
        index1, index2, binary_body, body1_ID, body2_ID, potential = get_binary(body_list)
        if index1 is None:
            break

        # Storing the data
        binary_index[binary_body.ID] = [[str(body1_ID) + "-" + str(body2_ID)],
                                        potential]

        # Replacing the 2 most bound with a single binary object
        body_list.append(binary_body)
        all_bodies.append(binary_body)

        # Sorting and reversing the indexes to guarantee the indexes
        # do not change after the first del()
        for i in sorted([index1, index2], reverse=True):
            del body_list[i]

        # Checking for highest order binary - Should == N
        if binary_body.order > highest_order:
            highest_order = binary_body.order
        counter += 1
    return all_bodies, binary_index


def get_binary(body_list):
    target1_ID, target2_ID, pot = get_most_bound(body_list)
    if pot is None:
        return [None]*6
    index1, index2, binary_body = get_index(target1_ID,
                                            target2_ID,
                                            body_list)
    return index1, index2, binary_body, target1_ID, target2_ID, pot


def get_most_bound(body_list):
    EP_dict = get_all_pot_energy(body_list)
    if EP_dict == {}:
        return None, None, None
    target1_ID, target2_ID, potential = get_largest_potential(EP_dict)
    return target1_ID, target2_ID, potential


def get_all_pot_energy(body_list):
    pair_energy_dict = {}
    done_pairs = []
    for i in body_list:
        main_body = i

        for j in body_list:
            target_body = j
            pair_ref = sorted([main_body.ID, target_body.ID])

            # Ensuring no 1-->2 and 2-->1 calculation
            # No interaction with self either
            if (i == j) or (pair_ref in done_pairs):
                pass
            else:
                pair_energy = of.get_grav_potential(
                        main_body.mass, target_body.mass,
                        main_body.position, target_body.position)
                if pair_energy < -1e28:
                    pair_energy_dict["{}-{}".format(main_body.ID,
                                     target_body.ID)] = pair_energy
            done_pairs.append(pair_ref)
    return pair_energy_dict


def get_largest_potential(dictionary):
    potential_list = list(dictionary.values())
    potential_list.sort()
    target_potential = potential_list[0]
    for ID, pot in dictionary.items():
        if pot == target_potential:
            target_ID = ID
            break
    if target_ID is None:
        raise ValueError("Target bodies not found in: get_largest_potential")
    target1_ID, target2_ID = target_ID.split("-")
    target1_ID, target2_ID = int(target1_ID), int(target2_ID)
    return target1_ID, target2_ID, target_potential


def get_index(id1, id2, body_list):
    body1, body2 = None, None
    for index, body in enumerate(body_list):
        if body.ID == id1:
            index1 = index
            body1 = body
        elif body.ID == id2:
            index2 = index
            body2 = body
    binary_body = combine(body1, body2)
    return index1, index2, binary_body


def create_body_objects(directory, index=-1):
    masses = of.get_single_data(directory + "/masses.csv")
    pos_x = of.get_single_data(directory + "/pos_x.csv")[index]
    pos_y = of.get_single_data(directory + "/pos_y.csv")[index]
    pos_z = of.get_single_data(directory + "/pos_z.csv")[index]
    vel_x = of.get_single_data(directory + "/vel_x.csv")[index]
    vel_y = of.get_single_data(directory + "/vel_y.csv")[index]
    vel_z = of.get_single_data(directory + "/vel_z.csv")[index]
    # Generating and storing all body objects in an array for easy access
    body_list_create = []
    for index, mass in enumerate(masses):
        pos = np.array([pos_x[index], pos_y[index], pos_z[index]], dtype="int64")
        vel = np.array([vel_x[index], vel_y[index], vel_z[index]], dtype="int64")
        temp_body = body_class(mass, pos, vel)
        body_list_create.append(temp_body)

    return body_list_create


def combine(body1, body2):
    mass, pos, vel, order_binary = merge(body1, body2)
    body_class.total_mass -= mass
    body_class.num_bodies -= 2
    base_components = str(body1.base) + str(body2.base)
    return body_class(mass, pos, vel, order=order_binary, base=base_components)


def merge(body1, body2):
    m1 = body1.mass
    m2 = body2.mass
    mass = m1 + m2
    order_binary = body1.order + body2.order
    pos = [(body1.position[0]*m1+body2.position[0]*m2)/mass,
           (body1.position[1]*m1+body2.position[1]*m2)/mass,
           (body1.position[2]*m1+body2.position[2]*m2)/mass]
    vel = [(body1.velocity[0]*m1+body2.velocity[0]*m2)/mass,
           (body1.velocity[1]*m1+body2.velocity[1]*m2)/mass,
           (body1.velocity[2]*m1+body2.velocity[2]*m2)/mass]
    return mass, pos, vel, order_binary


run_name = "3x3_standard"

body_list, binary_index = detect_binaries(run_name, 0)

# %%
# Generating all binary objects


binary_list = []
for ID in binary_index.keys():
    binary_list.append(binary(ID))

gr.plot_graph(run_name,
          display="All",
          x_dist=2e16,
          plot_pos=1,
          binary_to_plot=[6, 8, 7, 9, 3, 4],
          start=0)

gr.plot_secondary_graphs(run_name)
# %%



"""
count=0
plt.figure(1)
for obj in binary_list:
    if obj.order <= 2:
        plt.scatter(abs(obj.sma), obj.mr, color="black")
plt.xlabel("sma")
plt.ylabel("Mass ratio")
plt.grid()
plt.show()
"""