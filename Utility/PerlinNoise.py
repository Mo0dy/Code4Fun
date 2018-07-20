import numpy as np
import cv2 as cv
from itertools import product, count

from matplotlib.colors import LinearSegmentedColormap


# it produce more vectors pointing diagonally than vectors pointing along
# an axis
# # generate uniform unit vectors
# def generate_unit_vectors(n):
#     'Generates matrix NxN of unit length vectors'
#     v = np.random.uniform(-1, 1, (n, n, 2))
#     l = np.sqrt(v[:, :, 0] ** 2 + v[:, :, 1] ** 2).reshape(n, n, 1)
#     v /= l
#     return v

class PerlinNoise(object):

    def __init__(self, size, ns):
        self.size = size
        self.ns = ns
        self.nc = int(self.size / self.ns)  # number of nodes
        self.grid_size = int(size / ns + 1)
        phi = np.random.uniform(0, 2 * np.pi, (self.grid_size, self.grid_size))
        self.v = np.stack((np.cos(phi), np.sin(phi)), axis=-1)

    def update_unit_vectors(self):
        'Generates matrix NxN of unit length vectors'
        phi = np.random.uniform(0, 2*np.pi, (self.grid_size, self.grid_size))
        self.v += np.stack((np.cos(phi), np.sin(phi)), axis=-1) * 1

    # quintic interpolation
    def qz(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    # cubic interpolation
    def cz(self, t):
        return -2 * t * t * t + 3 * t * t

    def generate_2D_perlin_noise(self, dtype=np.float32):
        '''
        generate_2D_perlin_noise(size, ns)
        Generate 2D array of size x size filled with Perlin noise.
        Parameters
        ----------
        size : int
            Size of 2D array size x size.
        ns : int
            Distance between nodes.
        Returns
        -------
        m : ndarray
            The 2D array filled with Perlin noise.
        '''


        # generate grid of vectors
        self.update_unit_vectors()

        # generate some constans in advance
        ad, ar = np.arange(self.ns), np.arange(-self.ns, 0, 1)

        # vectors from each of the 4 nearest nodes to a point in the NSxNS patch
        vd = np.zeros((self.ns, self.ns, 4, 1, 2))
        for (l1, l2), c in zip(product((ad, ar), repeat=2), count()):
            vd[:, :, c, 0] = np.stack(np.meshgrid(l2, l1, indexing='xy'), axis=2)

        # interpolation coefficients
        d = self.qz(np.stack((np.zeros((self.ns, self.ns, 2)),
                         np.stack(np.meshgrid(ad, ad, indexing='ij'), axis=2)),
               axis=2) / self.ns)
        d[:, :, 0] = 1 - d[:, :, 1]
        # make copy and reshape for convenience
        d0 = d[..., 0].copy().reshape(self.ns, self.ns, 1, 2)
        d1 = d[..., 1].copy().reshape(self.ns, self.ns, 2, 1)

        # make an empy matrix
        m = np.zeros((self.size, self.size), dtype=dtype)
        # reshape for convenience
        t = m.reshape(self.nc, self.ns, self.nc, self.ns)

        # calculate values for a NSxNS patch at a time
        for i, j in product(np.arange(self.nc), repeat=2):  # loop through the grid
            # get four node vectors
            av = self.v[i:i+2, j:j+2].reshape(4, 2, 1)
            # 'vector from node to point' dot 'node vector'
            at = np.matmul(vd, av).reshape(self.ns, self.ns, 2, 2)
            # horizontal and vertical interpolation
            t[i, :, j, :] = np.matmul(np.matmul(d0, at), d1).reshape(self.ns, self.ns)

        return m

# noise = PerlinNoise(500, 20)
# for i in range(100):
#     img = noise.generate_2D_perlin_noise()
#     cv.imshow('test', img)
#     cv.waitKey(500)
#
# cv.destroyAllWindows()

# generate "sky"
#img0 = generate_2D_perlin_noise(400, 80)
#img1 = generate_2D_perlin_noise(400, 40)
#img2 = generate_2D_perlin_noise(400, 20)
#img3 = generate_2D_perlin_noise(400, 10)
#
#img = (img0 + img1 + img2 + img3) / 4
#cmap = LinearSegmentedColormap.from_list('sky',
#                                         [(0, '#0572D1'),
#                                          (0.75, '#E5E8EF'),
#                                          (1, '#FCFCFC')])
#img = cm.ScalarMappable(cmap=cmap).to_rgba(img)
#plt.imshow(img)