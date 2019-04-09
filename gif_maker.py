#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 21:27:21 2019

@author: josh
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import orbit_functions as of
import Integrator
import matplotlib.colors as colors
import random

run_name="run3"
run_dir = "./results/"
direc = run_dir + run_name
x = of.get_single_data(direc + "/pos_x.csv")
y = of.get_single_data(direc + "/pos_y.csv")
z = of.get_single_data(direc + "/pos_z.csv")
x, y, z = of.strip_trailing_data(x, y, z)

init_vars = of.get_init_conds(direc + "/init_conds.txt")
N = int(init_vars[1])
N_cluster = int(init_vars[0])