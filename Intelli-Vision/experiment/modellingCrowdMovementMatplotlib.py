import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# size of the crowd
N = 100


def gen_data():
    """init position and speed of each people"""
    x = y = np.zeros(N)
    theta = np.random.random(N) * 360 / (2 * np.pi)
    v0 = 0.1
    vx, vy = v0 * np.cos(theta), v0 * np.sin(theta)
    return np.column_stack([x, y, vx, vy])


def init():
    pathcol.set_offsets([[], []])
    return pathcol,


def update(i, pathcol, data):
    data[:, 0:2] += data[:, 2:4]
    data[:, 2] = np.where(np.abs(data[:, 0]) > 5, -data[:, 2], data[:, 2])
    data[:, 3] = np.where(np.abs(data[:, 1]) > 5, -data[:, 3], data[:, 3])
    pathcol.set_offsets(data[:, 0:2])
    return [pathcol]


fig = plt.figure()
ax = plt.axes(xlim=(-5, 5), ylim=(-5, 5))
pathcol = plt.scatter([], [])
data = gen_data()
x = data[:, 0]
anim = animation.FuncAnimation(fig, update, frames=len(x), init_func=init, fargs=(pathcol, data), interval=0, blit=True)
plt.show()
