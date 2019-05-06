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
import detection_functions as df
np.random.seed(124)

G = 6.674e-11
au = 1.49597e11
pc = 3.0857e16


run_name = ["3x4_standard", "3x3_standard", "1x5_seed1", "1x5_seed2", "1x5_seed3"]
#"3x4_standard", "3x3_standard", "1x5_seed1", "1x5_seed2", "1x5_seed3"]
#run_name = ["1x5_seed1"]

binary_list = []
#body_list = detect_binaries(run_name, 0)
for run in run_name:
    df.body_class.ID = 0
    binary_index = {}
    binaries = []
    body_list = []
    pairs = {}
    sorted_pairs = []
    sorted_pairs_fixed = []
    #body_list, binary_index = detect_binaries(run, -1)
    pairs, body_list = df.new_detect_binaries(run, -1)

    sorted_pairs = sorted(pairs.items(), key=lambda kv: kv[1])
    sorted_pairs_fixed = sorted_pairs[::2]

    for pair in sorted_pairs_fixed:
        target_ID = pair[0]
        potential = pair[1]
        if potential > -1e33:
            continue
        print (target_ID)
        target1_ID, target2_ID = target_ID.split("-")
        target1_ID, target2_ID = int(target1_ID), int(target2_ID)
        index1, index2, binary_body = df.get_index(target1_ID, target2_ID, body_list)
        binary_index[binary_body.ID] = [[str(target1_ID) + "-" + str(target2_ID)], potential]
    for ID in binary_index.keys():
        binary_list.append(df.binary(ID, binary_index, body_list))


# %%
"""
gr.plot_graph(run_name,
          display="All",
          x_dist=2e16,
          plot_pos=1,
          binary_to_plot=[6, 8, 7, 9, 3, 4],
          start=0)

gr.plot_secondary_graphs(run_name)

# %%
sma, potential, mr = [], [], []
for binary in binary_list:
    if abs(binary.sma) > 5000:
        continue
    else:
        sma.append(binary.sma)
        potential.append(abs(binary.EP))
        mr.append(binary.mr)
# %%
log_sma = np.log(sma)
log_pot = np.log(potential)
p, res, _, _, _ = np.polyfit(log_sma, log_pot, 1, full=True)
grad, intercept = p
fit = np.exp(grad*log_sma + intercept)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(sma, potential)
ax.plot(sma, fit)
#ax.set_yscale("log")
#ax.set_xscale("log")
ax.set_xlabel("Semi-major axis (au)")
ax.set_ylabel("Potential energy")
plt.annotate("y = {:.3} x^{:.3}".format(intercept, grad),
             xy=(0.5, 0.7),
             xycoords='axes fraction')
plt.title("Semi-major axis against potential energy of binary pairs")
plt.grid()
plt.show()
plt.savefig("results/graphs/{a}sma_pot.png".format(a="all_"))


fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(sma, mr)
plt.show()

"""