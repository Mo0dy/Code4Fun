import numpy as np

# creates transformation matrix from function parameters and couples it with a probability
def c_func(a, b, c, d, e, f):
    return np.array([[a, b, e],
                    [c, d, f],
                    [0, 0, 1]], dtype=np.float32)


def create_trans(input):
    trans = {"probs": [0],
             "mats": []}
    for i in input:
        trans["mats"].append(c_func(i[0], i[1], i[2], i[3], i[4], i[5]))
        trans["probs"].append(i[6] + trans["probs"][-1])
    trans["probs"] = trans["probs"][1:]
    trans["mats"] = np.array(trans["mats"], dtype=np.float32)
    trans["probs"] = np.array(trans["probs"], dtype=np.float32)
    if trans["probs"][-1] == 1:
        return trans
    else:
        return None


barnsleys_fern = create_trans([[0, 0, 0, 0.16, 0, 0, 0.01],
                              [0.85, 0.04, -0.04, 0.85, 0, 1.6, 0.85],
                              [0.2, -0.26, 0.23, 0.22, 0, 1.6, 0.07],
                              [-0.15, 0.28, 0.26, 0.24, 0, 0.44, 0.07]])

cyclosorus_fern = create_trans([[0, 0, 0, 0.25, 0, -0.4, 0.02],
                                [0.95, 0.005, -0.005, 0.93, -0.002, 0.5, 0.84],
                                [0.035, -0.2, 0.16, 0.04, -0.09, 0.02, 0.07],
                                [-0.04, 0.2, 0.16, 0.04, 0.083, 0.12, 0.07]])
