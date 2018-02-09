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
    'p_force_degree'
    'init_distrib',          # the initial distribution over the bounds
    'oob_force',            # oob forces
    'oob_force_mag',
    'multicolor',           # toggles multicolor support
    'color',                 # single color value
    'goal_forces',
    'goal_forces_mag',
    'goal_forces_disburse',
    'goal_forces_degree',
    'damping',
    'damping_mag',
}


# this class holds all the settings and updates it's particles. It can NOT be used to render them!
class ParticleSim(object):
    gravity = False
    grav_const = 9.81
    random_motion = True
    random_magnitude = 1
    # force to a point
    p_force = False
    p_force_mag = 1e3
    p_force_degree = 0
    # out of bounds forces
    oob_force = False
    oob_force_mag = 5e2
    init_distrib = 'ran_distrib'
    color = rnd.color([255, 255, 255])
    # forces to a certain color
    goal_forces = False
    goal_forces_mag = 1e4
    goal_forces_disburse = 1e3
    goal_forces_degree = 0
    damping = True
    damping_mag = 50

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
            else:
                sys.stderr.write('kw assignment "' + k + '" not found')
                sys.stderr.flush()

        # creating storage containers for the particle properties and assignes a distribution
        self.particles = getattr(self, self.init_distrib)()
        self.velocities = np.zeros((self.particle_amount, 2))
        self.forces = np.zeros((self.particle_amount, 2))

        self.colors = np.ones((self.particle_amount, 3), dtype=np.uint8) * 100
        self.goals = np.zeros((self.particle_amount, 2), dtype=np.float64)
        self.pursue_goals = np.zeros(self.particle_amount, dtype=np.bool)

    # calls all the different functions necessary to update the particles
    def update(self, dt):
        # these chained if statements could be implemented as a dictionary lookup for performance increase
        if self.gravity:
            ParticleSim.apply_gravity(self.forces, self.grav_const)
            # self.apply_gravity()
        if self.random_motion:
            ParticleSim.apply_random_forces(self.forces, self.random_magnitude)
        if self.p_force:
            if self.p_force_degree == 0:
                ParticleSim.apply_const_point_force(self.particles, self.forces, self.force_point, self.p_force_mag)
            else:
                ParticleSim.apply_poly_point_force(self.particles, self.forces, self.force_point, self.p_force_mag, self.p_force_degree)
        if self.oob_force:
            ParticleSim.apply_oob_force(self.particles, self.forces, self.x_bounds, self.y_bounds, self.oob_force_mag)
        if self.goal_forces:
            if self.goal_forces_degree == 0:
                ParticleSim.apply_const_goal_force(self.particles, self.forces, self.goals, self.pursue_goals, self.goal_forces_mag, self.goal_forces_disburse)
            else:
                ParticleSim.apply_poly_goal_force(self.particles, self.forces, self.goals, self.pursue_goals, self.goal_forces_mag, self.goal_forces_disburse, self.goal_forces_degree)

        if self.damping:
            ParticleSim.apply_damping_force(self.velocities, self.forces, self.damping_mag)
        ParticleSim.move_particles(self.particles, self.velocities, self.forces, dt)

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64)], '(a,b),(a,b),()', target='parallel', cache=True)
    def apply_damping_force(vel, f, mag):
        for i in nb.prange(vel.shape[0]):
            v_x = vel[i, 0]
            v_y = vel[i, 1]

            vel_mag = v_x ** 2 + v_y ** 2

            # if vel_mag:
            scale = mag * vel_mag

            # this can reverse the direction. Not accurate!
            f[i, 0] -= v_x * scale
            f[i, 1] -= v_y * scale

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:, :],  nb.float64[:], nb.float64, nb.float64)], '(a,b),(a,b),(a,b),(a),(),()', target='parallel', cache=True)
    def apply_const_goal_force(p, f, goals, pursue_goals, mag, disburse_mag):
        for i in nb.prange(p.shape[0]):
            d_x = goals[i, 0] - p[i, 0]
            d_y = goals[i, 1] - p[i, 1]

            dist_squared = d_x ** 2 + d_y ** 2
            if dist_squared:
                if pursue_goals[i]:
                    scale = mag / np.sqrt(dist_squared)
                else:
                    scale = -disburse_mag / dist_squared

                f[i, 0] += d_x * scale
                f[i, 1] += d_y * scale

    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:, :], nb.float64[:], nb.float64, nb.float64, nb.float64)],
                    '(a,b),(a,b),(a,b),(a),(),(),()', target='parallel', cache=True)
    def apply_poly_goal_force(p, f, goals, pursue_goals, mag, disburse_mag, poly_degree):
        for i in nb.prange(p.shape[0]):
            d_x = goals[i, 0] - p[i, 0]
            d_y = goals[i, 1] - p[i, 1]

            dist_squared = d_x ** 2 + d_y ** 2
            if dist_squared:
                if pursue_goals[i]:
                    scale = mag * np.sqrt(dist_squared) ** (poly_degree - 1)
                else:
                    scale = -disburse_mag / dist_squared

                f[i, 0] += d_x * scale
                f[i, 1] += d_y * scale

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

    # this only works for poly_degree >= 1
    @staticmethod
    @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:], nb.float64, nb.int64)], '(a,b),(a,b),(b),(),()', target='parallel', cache=True)
    def apply_poly_point_force(p, f, point, mag, poly_degree):
        for i in nb.prange(p.shape[0]):
            d_x = point[0] - p[i, 0]
            d_y = point[1] - p[i, 1]

            dist = (d_x ** 2 + d_y ** 2) ** poly_degree

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

    def __repr__(self):
        print(self.__dict__)

    # properties
    @property
    def x_bounds(self):
        return np.array([self.bounds_min.x, self.bounds_max.x])

    @property
    def y_bounds(self):
        return np.array([self.bounds_min.y, self.bounds_max.y])


@nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.boolean[:], nb.float64, nb.float64)], '(a,b),(d,e),(d),(),()', target='parallel', cache=False)
def assign_goals(input_arr, goal_points, pursue_goal, offset_x, offset_y):
    index = 0
    for i in nb.prange(pursue_goal.shape[0]):
        pursue_goal[i] = False

    for i in range(input_arr.shape[0]):
        for j in range(input_arr.shape[1]):
            if input_arr[i, j]:
                goal_points[index, 0] = i + offset_x
                goal_points[index, 1] = j + offset_y
                pursue_goal[index] = True
                index += 1




