# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:34:19 2019

@author: c1672922
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import orbit_functions as of
from matplotlib import animation

x = of.get_single_data("pos_x.csv")
y = of.get_single_data("pos_y.csv")
z = of.get_single_data("pos_z.csv")


fig = plt.figure()
ax = plt.axes()
#ax = plt.axes(xlim=(5.5e15, 5.75e15),
#              ylim=(-1e14, 1e14))
line, = ax.plot([], [])


def init():
    line.set_data([], [])
    return line,


def animate(i):
    x = of.get_single_data("pos_x.csv").T
    y = of.get_single_data("pos_y.csv").T
    line.set_data(x[0][i], y[0][i])
    return line,


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)
anim.save("test_animation.mp4", fps=30, extra_args=["-vcodec", "libx264"])


plt.figure(2)
plt.plot(x[::10, i], y[::10, i])

"""
fig - plt.figure()
ax = plt.axes(xlim=(min(x), max(x)),
              ylim=(min(y), max(y)), zlim=(min(z), max(z)))
line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = x[::, i]
    y = y[::, i]
    z = z[::, i]
    line.set_data(x, y, z)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, blit=True)

"""




"""
fig = plt.figure()
p1 = fig.add_subplot(111, projection="3d")
for i in range(len(x[0])):
    if i < 5: col="r"
    elif i >= 5 and i < 10: col = "b"
    elif i >= 10 and i < 15: col = "g"
    elif i >= 15 and i < 20: col = "c"
    elif i >= 20 and i < 25: col = "k"
    elif i >= 25 and i < 30: col = "m"
    else: col = "y"
    p1.scatter(x[::10, i], y[::10, i], z[::10, i], color=col)

fig.show()
fig = plt.savefig("positions.pdf")
"""