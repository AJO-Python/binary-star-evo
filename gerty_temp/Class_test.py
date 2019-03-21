#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:10:24 2019

@author: josh
"""

import numpy as np
import orbit_functions as of
np.random.seed(123)


class body:
    num_bodies = 0
    ID = 0

    def __init__(self, mass, position, velocity, order=1):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.ID = body.ID
        self.order = order
        self.potential = 0
        body.num_bodies += 1
        body.ID += 1

    def combine(self, body2):
        # Finds resultant mass, pos, vel
        # Combines into new body
        # Does not redefine "self" so unique ID is generated
        # for the binary body object
        mass = self.mass + body2.mass
        pos, vel = body.merge_pos_vel(self, body2)
        order = self.order + body2.order
        return body(mass, pos, vel, order)

    def merge_pos_vel(self, body2):
        pos = [[(self.position[0]+body2.position[0])/2],
                [(self.position[1]+body2.position[1])/2],
                [(self.position[2]+body2.position[2])/2]]
        vel = [[(self.velocity[0]+body2.velocity[0])/2],
                [(self.velocity[1]+body2.velocity[1])/2],
                [(self.velocity[2]+body2.velocity[2])/2]]
        return pos, vel


def main():
    body_list = create_body_objects()
    master_list = body_list  # Creating master_copy as a backup
    while len(body_list) > 2:  # Recalculating after every binary is found
        # Get unique ID of two most bound bodies
        for i in body_list:
            print (i.mass)
        print ()
        binary_body, index1, index2 = get_binary(body_list)
        body_list.append(binary_body)
        body_list = np.delete(body_list, (t1_ID, t2_ID), 0)
        body_list_temp = body_list
    return body_list


def get_binary(body_list):
    t1_ID, t2_ID, pot = get_most_bound(body_list)
    binary_body, index1, index2 = get_index(t1_ID, t2_ID, body_list)
    binary_body.potential += pot
    return binary_body, index1, index2


def get_most_bound(body_list):
        EP_dict = get_all_pot_energy(body_list)
        target1_ID, target2_ID, potential = sort_by_energy(EP_dict)
        return target1_ID, target2_ID, potential


def get_all_pot_energy(body_list):
    pair_energy_dict = {}
    for i in body_list:
        main_body = i
        for j in body_list:
            target_body = j
            if i == j:
                pass
            else:
                pair_energy = of.get_grav_potential(
                    main_body.mass, target_body.mass,
                    main_body.position, target_body.position)
                pair_energy_dict["{}-{}".format(main_body.ID,
                                 target_body.ID)] = pair_energy
                print (i.ID, j.ID)
                print (pair_energy)
    return pair_energy_dict

def sort_by_energy(dictionary):
    potential_list = list(dictionary.values())
    #print (potential_list)
    potential_list.sort()
    #print (potential_list)
    target_potential = potential_list[0]
    for ID, pot in dictionary.items():
        if pot == target_potential:
            target_ID = ID
    target1_ID, target2_ID = target_ID.split("-")
    target1_ID, target2_ID = int(target1_ID), int(target2_ID)
    return target1_ID, target2_ID, target_potential


def get_index(id1, id2, body_list):
        for index, body in enumerate(body_list):
            if body.ID == id1:
                index1 = index
                body1 = body
            elif body.ID == id2:
                index2 = index
                body2 = body
        body = body1.combine(body2)
        return body, index1, index2


def create_body_objects():
    masses = of.get_single_data("masses.csv")
    pos_x = of.get_single_data("pos_x.csv")[-1]  # Position has time-varying
    pos_y = of.get_single_data("pos_y.csv")[-1]  # data. Take the [-1] index
    pos_z = of.get_single_data("pos_z.csv")[-1]  # to get last position
    vel_x = of.get_single_data("vel_x.csv")
    vel_y = of.get_single_data("vel_y.csv")
    vel_z = of.get_single_data("vel_z.csv")
    # Generating and storing all body objects in an array for easy access
    body_list = []
    for index, mass in enumerate(masses):
        temp_body = body(mass,
                         [pos_x[index], pos_y[index], pos_z[index]],
                         [vel_x[index], vel_y[index], vel_z[index]])
        body_list.append(temp_body)

    return body_list


bosy_list = main()






















