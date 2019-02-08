import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy


max_iter = 2000
radius = 45
end_radius = 2
small_radius = 10
end_small_radius = 1
rot_iter = 30
height = 180
turns = 15

ratio = 1.61803

def cross_product(a, b):
    return np.array([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]])


def rotate(angle, v, axis):
    return v * np.cos(angle) + cross_product(axis, v) * np.sin(angle) + axis * (axis @ v) * (1 - np.cos(angle))


def get_z_pos(iteration):
    prop = iteration / max_iter
    return prop ** 2 * height
    # return prop * height
    
def get_small_radius(iteration):
    prop = iteration / max_iter
    if prop > 0.2:
        return prop * (small_radius - end_small_radius) + end_small_radius
    else:
        return np.sqrt(prop) * (small_radius - end_small_radius) + end_small_radius
    # return ratio ** (turns / max_iter * iteration) * 0.01

def get_radius(iteration):
    # return end_radius + (radius - end_radius) / max_iter * iteration
    return (iteration / max_iter) ** 2 * 50


def base_curve(iteration):
    angle = np.pi * 2 / max_iter * iteration * turns
    # angle_2 = np.pi * 2 / max_iter * (iteration + 1)
    # z_pos_2 = height / max_iter * (iteration + 1)
    # z_pos = height / max_iter * iteration
    z_pos = get_z_pos(iteration)
    offset_angle = angle + np.pi / 2
    r = get_radius(iteration)
    pos = np.array([np.sin(angle) * r, np.cos(angle) * r, z_pos])
    # next_pos = np.array([np.sin(angle_2) * radius, np.cos(angle_2) * radius, z_pos_2])
    # vector = next_pos - pos
    # vector /= vector @ vector
    vector = np.array([np.sin(offset_angle), np.cos(offset_angle), 0])
    return pos, vector


vertices = []
faces = []
first = True
for i in range(max_iter): # range(max_iter - 1):
    pos, vec = base_curve(i)
    start_index = len(vertices)
    old_start_index = start_index - rot_iter
    # print("start index", start_index)
    # print("old_index", old_start_index)
    for j in range(rot_iter):
        angle = np.pi * 2 / (rot_iter) * j
        # print(angle)
        # vec is a unit vector. from there calculate the othogonal vector on the curve
        # oth = np.array([vec[0] * vec[2], vec[1] * vec[2], np.sqrt(np.sum(vec @ vec)) * small_radius])
        oth = np.array([0, 0, get_small_radius(i)])
        vertices.append(rotate(angle, oth, vec) + pos)
        # vertices.append([np.cos(angle) * 100, np.sin(angle) * 100, i * 50])
        if not first:
            # print("triganle:", [start_index + j, old_start_index + j, old_start_index + (j + 1) % rot_iter])
            a = start_index + j
            b = old_start_index + j
            c = old_start_index + (j + 1) % rot_iter
            d = start_index + (j + 1) % rot_iter
            faces.append([a, b, c])
            faces.append([a, c, d])
    if first:
        first = False

vertices = np.array(vertices)
faces = np.array(faces)

# print(vertices)
# print(faces)

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]

# Write the mesh to file "cube.stl"
cube.save('cube.stl')

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter([v[0] for v in vertices], [v[1] for v in vertices], [v[1] for v in vertices])
# plt.show()
