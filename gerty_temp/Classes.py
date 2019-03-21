# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 12:38:27 2019

@author: Josh
"""
import numpy as np
import orbit_functions as of
np.random.seed(123)


class coord:
    def __init__(self, vector):
        self.x = vector[0]
        self.y = vector[1]
        self.z = vector[2]
        self.vec = vector


class body:
    num_of_bodies = 0

    def __init__(self, mass, position, velocity, identity="", order=1):
        self.mass = mass
        self.pos = coord(position)
        self.vel = coord(velocity)
        self.id = identity
        self.order = order

        body.num_of_bodies += 1


class binary:
    num_of_binaries = 0

    def __init__(self, index1, index2, energy):
        self.pair = [index1, index2]
        self.energy = energy
        self.mass = body_list[index1].mass + body_list[index2].mass
        self.vel = np.add(body_list[index1].vel.vec, body_list[index2].vel.vec)
        self.pos = body_list[index1].pos.vec + body_list[index2].pos.vec
        self.bin_id = np.array((body_list[index1].id, body_list[index2].id))
        self.order = body_list[index1].order + body_list[index2].order
        binary.num_of_binaries += 1

    def combine_binary(self, body_list):
        i, j = self.pair
        print("indicies to combine: ", i, j)
        main, target = body_list[i], body_list[j]
        mass = (main.mass + target.mass)*0.5
        pos = np.add(main.pos.vec, target.pos.vec)*0.5
        vel = np.add(main.vel.vec, target.vel.vec)*0.5
        binary_point = body(mass, pos, vel, identity=[i, j])
        return binary_point

    def replace_pair(self, body_list):
        body1, body2 = body_list(self.pair)

    def __eq__(self, other):
        return self.energy == other.energy

    def __lt__(self, other):
        return self.energy < other.energy


def condense_binaries(body_list):
    binaries_long = []
    temp_list = body_list
    while len(temp_list) > 1:
        binary = get_most_bound(temp_list)
        np.append(temp_list, binary)
        temp_list = np.delete(temp_list, binary.id)
        binaries_long.append(binary.id)
        print("len of body list: ", len(temp_list))
    return binaries_long


def get_most_bound(body_list):
        EP_list = get_all_pot_energy(body_list)
        EP_sorted = sorted(EP_list, key=lambda x: x.energy)
        most_bound_pair = EP_sorted[0]
        binary_point = most_bound_pair.combine_binary(body_list)
        return binary_point


def get_all_pot_energy(body_list):
    binary_list = []
    for i in body_list:
        main_body = i
        for j in body_list:
            target_body = j
            if i == j:
                pass
            else:
                pair_energy = of.get_grav_potential(
                    main_body.mass, target_body.mass,
                    main_body.pos.vec, target_body.pos.vec)
                binary_list.append(binary(
                        main_body.id, target_body.id, pair_energy)
                                    )
    return binary_list

# %%


masses = of.get_single_data("masses.csv")
pos_x = of.get_single_data("pos_x.csv")[-1]  # Position has time-varying data
pos_y = of.get_single_data("pos_y.csv")[-1]  # take the [-1] index to get
pos_z = of.get_single_data("pos_z.csv")[-1]  # last position
vel_x = of.get_single_data("vel_x.csv")
vel_y = of.get_single_data("vel_y.csv")
vel_z = of.get_single_data("vel_z.csv")

# Generating and storing all body objects in an array for easy access
body_list = []
for index, mass in enumerate(masses):
    temp_body = body(mass,
                     [pos_x[index], pos_y[index], pos_z[index]],
                     [vel_x[index], vel_y[index], vel_z[index]], index)
    body_list.append(temp_body)

body_list = np.asarray(body_list, dtype=object)
"""
Body_list = list of all stars with their details
binary_list = list of binary pairs with ID and energy

"""


binaries = condense_binaries(body_list)


















