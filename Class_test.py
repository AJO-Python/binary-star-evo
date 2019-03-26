#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:10:24 2019

@author: josh
"""

import numpy as np
import orbit_functions as of
import sys
np.random.seed(123)


class body:
    # Class count of how many bodies have been created
    # and what the unique ID counter and total system mass are
    num_bodies = 0
    ID = 0
    total_mass = 0

    def __init__(self, mass, position, velocity, order=1, base=""):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.ID = body.ID
        self.order = order
        # Checking if the star is a single or multiple already
        if self.order == 1:
            self.base = str(self.ID)  # setting the base to the ID if single
        else:
            self.base = base # Setting base to the passed in argument
                             # of "base". This is the IDs of the base objects
        # Mainting the class counters
        body.num_bodies += 1
        body.ID += 1
        body.total_mass += mass

    def show_atts(self):
        # Used to print all attributes of a body
        print("ID: ", self.ID)
        print("Order: ", self.order)
        print("Base: ", self.base)
        print("Mass: ", self.mass)
        print("Position: ", self.position)
        print("Velocity: ", self.velocity)
        print()


def main_loop(run_name):  # e.g "results2.py"
    body_list = create_body_objects("./results/" + run_name)

    all_bodies = [body for body in body_list]
    binary_index = {}
    inital_bodies = len(body_list)
    highest_order = 0
    counter = 0

    while len(body_list) > 1:  # Recalculating after every binary is found
        binary_body = None  # Clearing the variable
        # Getting the most bound binary and the indexes of the bodies
        index1, index2, binary_body, body1_ID, body2_ID = get_binary(body_list)
        # Storing the data
# ------> all_bodies.append(binary_body)
        binary_index[binary_body.ID] = str(body1_ID) + "-" + str(body2_ID)
        # Replacing the 2 most bound with a single binary object
        body_list.append(binary_body)
        all_bodies.append(binary_body)
        # Sorting and reversing the indexes to guarantee the indexes
        # do not change after the first del()
        for i in sorted([index1, index2], reverse=True):
            del body_list[i]
        if binary_body.order > highest_order:
            highest_order = binary_body.order
        counter += 1
    return all_bodies, binary_index


def get_binary(body_list):
    target1_ID, target2_ID, pot = get_most_bound(body_list)
    index1, index2, binary_body = get_index(target1_ID,
                                                      target2_ID,
                                                      body_list)
    return index1, index2, binary_body, target1_ID, target2_ID


def get_most_bound(body_list):
        EP_dict = get_all_pot_energy(body_list)
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

            if (i == j) or (pair_ref in done_pairs):
                pass
            else:
                pair_energy = of.get_grav_potential(
                        main_body.mass, target_body.mass,
                        main_body.position, target_body.position)

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


def create_body_objects(directory):
    masses = of.get_single_data(directory + "/masses.csv")
    pos_x = of.get_single_data(directory + "/pos_x.csv")[-1]  # Position has time-varying
    pos_y = of.get_single_data(directory + "/pos_y.csv")[-1]  # data. Take the [-1] index
    pos_z = of.get_single_data(directory + "/pos_z.csv")[-1]  # to get last position
    vel_x = of.get_single_data(directory + "/vel_x.csv")
    vel_y = of.get_single_data(directory + "/vel_y.csv")
    vel_z = of.get_single_data(directory + "/vel_z.csv")
    # Generating and storing all body objects in an array for easy access
    body_list_create = []
    for index, mass in enumerate(masses):
        temp_body = body(mass,
                         [pos_x[index], pos_y[index], pos_z[index]],
                         [vel_x[index], vel_y[index], vel_z[index]])
        body_list_create.append(temp_body)

    return body_list_create

def combine(body1, body2):
    mass, pos, vel, order_binary = merge(body1, body2)
    body.total_mass -= mass
    body.num_bodies -= 2
    base_components = str(body1.base) + str(body2.base)
    return body(mass, pos, vel, order=order_binary, base=base_components)

def merge(body1, body2):
    mass = body1.mass + body2.mass
    order_binary = body1.order + body2.order
    pos = [(body1.position[0]+body2.position[0])/2,
            (body1.position[1]+body2.position[1])/2,
            (body1.position[2]+body2.position[2])/2]
    vel = [(body1.velocity[0]+body2.velocity[0])/2,
            (body1.velocity[1]+body2.velocity[1])/2,
            (body1.velocity[2]+body2.velocity[2])/2]
    return mass, pos, vel, order_binary


body_list, binary_index = main_loop("run4")

