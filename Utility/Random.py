import random


def random_int(*args):
    if len(args) == 1:
        return int(random.random() * (args[0] + 1))
    elif len(args) == 2:
        return int(random.random() * (args[1] - args[0] + 1) + args[0])
    else:
        print("random_int: ERROR TOO MANY ARGUMENTS")


def random_num(*args):
    if len(args) == 1:
        return random.random() * args[0]
    elif len(args) == 2:
        return random.random() * (args[1] - args[0]) + args[0]
    else:
        print("random_num: ERROR TOO MANY ARGUMENTS")


def random_vec2(length=1):  # Returns a random Vec2 with length len
    # The random vector needs to be determined via a random angle. Random x and y values will not lead to a vector with
    # a truly random direction / angle
    random_angle = random_num(2 * math.pi)
    r_v = Vec2(0, 1) * length
    r_v.theta = random_angle
    return r_v