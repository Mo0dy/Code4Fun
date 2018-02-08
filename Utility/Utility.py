import numpy as np
import numba as nb


# functions that assign color
def flame_color(temp):
    if temp < 127.5:
        return temp, 0, 0
    elif temp < 255:
        return 255, np.clip(510 - temp, 0, 255), 0


def flame_color_vec(temps):
    colors = np.zeros((temps.shape[0], 3))
    lower_temps = temps < 127.5
    colors[lower_temps, 0] = temps[lower_temps]
    higher_temps = np.logical_not(lower_temps)
    colors[higher_temps, 0] = 255
    colors[higher_temps, 1] = 510 - temps[higher_temps]
    return np.array(colors, dtype=np.uint8)

