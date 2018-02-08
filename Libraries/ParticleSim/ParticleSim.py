import numpy as np
import numba as nb


# the settings that are whitelisted to be passed directly via kwargs
# this is a stack for better lookup performance
allowed_settings = {'position'}


# this class holds all the settings and updates it's particles. It can NOT be used to render them!
class ParticleSimulation(object):
    def __init__(self, **kwargs):

        # assigns kwargs to member variables if allowed
        for k, var in kwargs.items():
            if k in allowed_settings:
                self.__dict__[k] = var



if __name__ == "__main__":
    pSim = ParticleSimulation(
        # size=
    )
    print(pSim.position)













