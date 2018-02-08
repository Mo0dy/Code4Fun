import numpy as np
import numba as nb
from Code4Fun.Utility.Vec2 import *


# the settings that are whitelisted to be passed directly via kwargs
# this is a stack for better lookup performance
allowed_settings = {
    'gravity',              # toggles gravity
    'grav_const',           # the strength of gravity
    'random_motion',        # toggle random motion
    'random_magnitude',     # the strength of the random motion
}


# this class holds all the settings and updates it's particles. It can NOT be used to render them!
class ParticleSim(object):
    grav_const = 9.81
    gravity = False
    random_motion = False
    random_magnitude = 10
    init_distrib = 'ran_distro'

    def __init__(self, x_bounds=(0, 800), y_bounds=(0, 800), particle_amount=1e5, **kwargs):
        # assigns kwargs to member variables if allowed
        # the boundaries of the system these will be used to create particles find oob particles and apply edge forces
        self.bounds_min = Vec2(x_bounds[0], y_bounds[0])
        self.bounds_max = Vec2(x_bounds[1], y_bounds[1])
        self.particle_amount = int(particle_amount)

        for k, var in kwargs.items():
            if k in allowed_settings:
                self.__dict__[k] = var

        # creating storage containers for the particle properties and assignes a distribution
        self.particles = getattr(self, self.init_distrib)()
        self.velocities = np.zeros((self.particle_amount, 2))
        self.forces = np.zeros((self.particle_amount, 2))

    # calls all the different functions necessary to update the particles
    def update(self, dt):
        # these chained if statements could be implemented as a dictionary lookup for performance increase
        if self.gravity:
            self.apply_gravity()
        if self.random_motion:
            self.apply_random_forces()
        self.move_particles(dt)

    # adds various forces to the particles
    def apply_gravity(self):
        self.forces[:, 1] += self.grav_const

    def apply_random_forces(self):
        # this is not truly random but biased to diagonal movement
        self.forces += np.random.rand(self.particle_amount, 2) * self.random_magnitude * 2 - self.random_magnitude

    # this function actually moves the particles
    def move_particles(self, dt):
        self.velocities += self.forces * dt
        self.particles += self.velocities * dt
        self.forces = np.zeros((self.particle_amount, 2))

    # particle_init functions
    # a random distribution over the bounds
    def ran_distro(self):
        particles = np.random.rand(self.particle_amount, 2)
        # scales the normalized random values in between the bounds
        particles[:, 0] = particles[:, 0] * (self.bounds_max.x - self.bounds_min.x) + self.bounds_min.x
        particles[:, 1] = particles[:, 1] * (self.bounds_max.y - self.bounds_min.y) + self.bounds_min.y
        return particles

    def lin_distro(self):
        pass


if __name__ == "__main__":
    pSim = ParticleSim(
        # size=
    )













