import numpy as np
import numba as nb
from Code4Fun.Utility.Vec2 import *
import Code4Fun.Utility.Renderer as rnd
import sys


# the settings that are whitelisted to be passed directly via kwargs
# this is a stack for better lookup performance
allowed_settings = {
    'gravity',              # toggles gravity
    'grav_const',           # the strength of gravity
    'random_motion',        # toggle random motion
    'random_magnitude',     # the strength of the random motion
    'p_force',              # linear forces to a point
    'p_force_mag',          # mag of the linear forces
    'init_distrib',          # the initial distribution over the bounds
    'oob_force',            # oob forces
    'oob_force_mag',
    'multicolor',           # toggles multicolor support
    'color'                 # single color value
}


# this class holds all the settings and updates it's particles. It can NOT be used to render them!
class ParticleSim(object):
    gravity = False
    grav_const = 9.81
    random_motion = False
    random_magnitude = 10
    p_force = False
    p_force_mag = 10
    oob_force = False
    oob_force_mag = 100
    init_distrib = 'ran_distrib'
    multicolor = False
    color = rnd.color([255, 255, 255])
    goal_forces = False
    goal_forces_mag = 10

    def __init__(self, x_bounds=(0, 800), y_bounds=(0, 800), particle_amount=1e5, **kwargs):
        # assigns kwargs to member variables if allowed
        # the boundaries of the system these will be used to create particles find oob particles and apply edge forces
        self.bounds_min = Vec2(x_bounds[0], y_bounds[0])
        self.bounds_max = Vec2(x_bounds[1], y_bounds[1])
        self.particle_amount = int(particle_amount)
        middle_point = (self.bounds_min + self.bounds_max) / 2
        self.force_point = np.array([middle_point.x, middle_point.y])

        for k, var in kwargs.items():
            if k in allowed_settings:
                self.__dict__[k] = var

        # creating storage containers for the particle properties and assignes a distribution
        self.particles = getattr(self, self.init_distrib)()
        self.velocities = np.zeros((self.particle_amount, 2))
        self.forces = np.zeros((self.particle_amount, 2))

        if self.multicolor:
            self.colors = np.ones((self.particle_amount, 3), dtype=np.uint8) * 100

        if self.goal_forces:
            self.goals = np.zeros((self.particle_amount, 2))

    # calls all the different functions necessary to update the particles
    def update(self, dt):
        # these chained if statements could be implemented as a dictionary lookup for performance increase
        if self.gravity:
            ParticleSim.apply_gravity(self.forces, self.grav_const)
            # self.apply_gravity()
        if self.random_motion:
            ParticleSim.apply_random_forces(self.forces, self.random_magnitude)
        if self.p_force:
            ParticleSim.apply_const_point_force(self.particles, self.forces, self.force_point, self.p_force_mag)
        if self.oob_force:
            ParticleSim.apply_oob_force(self.particles, self.forces, self.x_bounds, self.y_bounds, self.oob_force_mag)
        ParticleSim.move_particles(self.particles, self.velocities, self.forces, dt)

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:, :], nb.float64)], '(a,b),(a,b),(a,b),()', target='parallel', cache=True)
    def apply_const_goal_force(p, f, goals, mag):
        for i in nb.prange(p.shape[0]):
            d_x = goals[i, 0] - p[i, 0]
            d_y = goals[i, 1] - p[i, 1]

            dist = np.sqrt(d_x ** 2 + d_y ** 2)

            # normalizes and then scales the force vector
            d_x *= mag / dist
            d_y *= mag / dist

            f[i, 0] += d_x
            f[i, 1] += d_y

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:], nb.float64[:], nb.float64)], '(a,b),(a,b),(b),(b),()', target='parallel', cache=True)
    def apply_oob_force(p, f, x_bounds, y_bounds, mag):
        for i in nb.prange(p.shape[0]):
            # left oob
            if p[i, 0] < x_bounds[0]:
                f[i, 0] += (x_bounds[0] - p[i, 0]) * mag

            # right oob
            elif p[i, 0] > x_bounds[1]:
                f[i, 0] += (x_bounds[1] - p[i, 0]) * mag

            # up oob
            if p[i, 1] < y_bounds[0]:
                f[i, 1] += (y_bounds[0] - p[i, 1]) * mag

            # down oob
            elif p[i, 1] > y_bounds[1]:
                f[i, 1] += (y_bounds[1] - p[i, 1]) * mag

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:], nb.float64)], '(a,b),(a,b),(b),()', target='parallel', cache=True)
    def apply_const_point_force(p, f, point, mag):
        for i in nb.prange(p.shape[0]):
            d_x = point[0] - p[i, 0]
            d_y = point[1] - p[i, 1]

            dist = np.sqrt(d_x ** 2 + d_y ** 2)

            # normalizes and then scales the force vector
            d_x *= mag / dist
            d_y *= mag / dist

            f[i, 0] += d_x
            f[i, 1] += d_y

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64)], '(a,b),()', target='parallel', cache=True)
    def apply_gravity(f, mag):
        for i in nb.prange(f.shape[0]):
            f[i, 1] += mag

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64)], '(a,b),()', target='parallel', cache=True)
    def apply_random_forces(f, mag):
        mag2 = mag * 2
        for i in nb.prange(f.shape[0]):
            f[i, 0] += (np.random.rand() - 0.5) * mag2
            f[i, 1] += (np.random.rand() - 0.5) * mag2

    # this function actually moves the particles
    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:, :], nb.float64)], '(a,b),(a,b),(a,b),()', target='parallel', cache=True)
    def move_particles(p, vel, f, dt):
        for i in nb.prange(p.shape[0]):
            vel[i, 0] += f[i, 0] * dt
            vel[i, 1] += f[i, 1] * dt

            p[i, 0] += vel[i, 0] * dt
            p[i, 1] += vel[i, 1] * dt

            f[i, 0] = 0
            f[i, 1] = 0

    # particle_init functions
    # a random distribution over the bounds
    def ran_distrib(self):
        particles = np.random.rand(self.particle_amount, 2)
        # scales the normalized random values in between the bounds
        particles[:, 0] = particles[:, 0] * (self.bounds_max.x - self.bounds_min.x) + self.bounds_min.x
        particles[:, 1] = particles[:, 1] * (self.bounds_max.y - self.bounds_min.y) + self.bounds_min.y
        return particles

    def lin_distrib(self):
        pass

    # multicolor functions:
    def ran_color_distrib(self):
        self.colors = (np.random.rand(self.particle_amount, 3) * 255).astype(np.uint8)

    # properties
    @property
    def x_bounds(self):
        return np.array([self.bounds_min.x, self.bounds_max.x])

    @property
    def y_bounds(self):
        return np.array([self.bounds_min.y, self.bounds_max.y])


def find_goal_forces(input_arr, goal_points):
    index = 0
    for i in range(input_arr.shape[0]):
        for j in range(input_arr.shape[1]):
            if index >= goal_points.shape[0]:
                sys.stdout.error.write("index oob: goal array")
                sys.stdout.error.flush()
            if input_arr[i, j]:
                goal_points[index, 0] = i
                goal_points[index, 1] = j
                index += 1
















