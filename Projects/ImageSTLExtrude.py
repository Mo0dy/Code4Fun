import numpy as np
from stl import mesh
import cv2 as cv

vertices = []
faces = []

# code here
img = np.array(cv.imread(r"C:\Users\felix\Desktop\dndlogo.png"))[:, :, 0]
# add padding
img = cv.copyMakeBorder(img, 1, 1, 1, 1, cv.BORDER_CONSTANT, value=255)

img = img == 0

kernel = np.array([[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]])

# count neighbours and remove every cell with four neighbours (value of five because self also needs to be 1)
img[cv.filter2D(img.astype(np.uint8), -1, kernel) == 5] = False


def early_fix():
    global img
    """at the end every pixel will only have 2 neighbours"""
    # remove small features
    kernel_small_features = np.ones((3, 3))
    iteration = 0
    while True:
        small_features = np.logical_and(cv.filter2D(img.astype(np.uint8), -1, kernel_small_features) == 2, img)
        if not np.any(small_features):
            print("REMOVED small features after %i iterations" % iteration)
            break
        img[small_features] = False
        iteration += 1


early_fix()

begin_copy = img.copy()

# the image now only has the outlines of the shape

loops = []


def fix_image():
    section = img[start_vertex[0] - 10: start_vertex[0] + 11, start_vertex[1] - 10: start_vertex[1] + 11]
    section_orig = begin_copy[start_vertex[0] - 10: start_vertex[0] + 11, start_vertex[1] - 10: start_vertex[1] + 11].astype(np.uint8) * 255

    print(begin_copy)

    scale = 10
    section_orig = cv.resize(section_orig, (0, 0), fx=scale, fy=scale, interpolation=cv.INTER_NEAREST)
    section_orig = np.hstack((np.ones((section_orig.shape[0], 5)).astype(np.uint8) * 100, section_orig))

    def show():
        s_img = section.astype(np.uint8) * 255
        s_img[10, 10] = 150
        cv.imshow("fix", np.hstack((cv.resize(s_img, (0, 0), fx=scale, fy=scale, interpolation=cv.INTER_NEAREST), section_orig)))

    show()

    def pos_to_px(x, y):
        return y // scale, x // scale

    def mouse_callback(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            pos = pos_to_px(x, y)
            section[pos] = not section[pos]
            show()

    cv.setMouseCallback('fix', mouse_callback)

    while True:
        k = cv.waitKey(100)
        if k != -1:
            break


while True:
    start_vertex = np.unravel_index(np.argmax(img), img.shape)
    if not np.any(start_vertex):
        break
    loop = []  # a closed loop of vertices that surrounds the current selection

    while True:
        loop.append(start_vertex)
        img[start_vertex] = False
        # find the next neighbouring black spot. ignoring edges for now. (they will just be added in the beginning)
        neighbours = img[start_vertex[0] - 1: start_vertex[0] + 2, start_vertex[1] - 1: start_vertex[1] + 2]
        if not np.any(neighbours):  # done
            break
        # if np.sum(neighbours) > 1:
        #     # there needs to be a decision on how to change the image:
        #     fix_image()
        #     loop = loop[:-1]
        #     continue
        n_max_pos = np.unravel_index(np.argmax(neighbours), neighbours.shape)
        n_dir = n_max_pos + np.array([-1, -1])
        start_vertex = tuple(start_vertex + n_dir)

    loops.append(loop)

# save the fixed image
cv.imwrite(r"C:\Users\felix\Desktop\dndlogofixed.png", np.logical_not(img).astype(np.uint8) * 255)

# extrude loop:
offset = 0  # the offset in the vertex count
for l in loops:
    n = len(l)  # the amount of base vertices
    # the vertices of the bottom and top
    vertices += [[p[0], p[1], 0] for p in l] + [[p[0], p[1], 100] for p in l]

    # create triangles between the vertices
    for i in range(n):
        a = i + offset
        b = (i + 1) % n + offset
        c = (i + 1) % n + n + offset
        d = i + n + offset

        faces.append([a, b, c])
        faces.append([a, c, d])

    # advance offset
    offset += n * 2


# export the vertices and faces
vertices = np.array(vertices)
faces = np.array(faces)

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file "cube.stl"
cube.save('cube.stl')
