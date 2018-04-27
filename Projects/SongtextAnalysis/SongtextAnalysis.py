import numpy as np
import pygame as pg
import sys
import Code4Fun.Utility.Color as Color
import random
import string

background_color = 50, 50, 50
window_size = 800, 800
fps_cap = 5


pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Songtext Wordcount Analysis")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)


# settings
filepath = "SongtextBohemian.txt"

max_words = 800


def init():
    global counts
    with open(filepath, 'r') as file:
        lines = file.readlines()

    words = []

    for l in lines:
        words += l.split(" ")

    for i in range(len(words)):
        if "\n" in words[i]:
            words[i] = words[i][:-1]

    counts = {}

    for w in words:
        stripped_word = ''.join(filter(str.isalpha, w.lower()))
        if stripped_word != "":
            if stripped_word in counts:
                counts[stripped_word] += 1
            else:
                counts[stripped_word] = 1

    # sorts the dictionary by values (reverses the sorting thing)
    sorted_counts = sorted(counts.items(), key=lambda t: (t[1], t[0]), reverse=True)

    total_count = len(words)

    # the count of bars
    hist_count = len(sorted_counts)

    # assumes square window size
    amount_per_side = int(np.ceil(np.sqrt(max_words)))
    square_side_length = int(window_size[1] / amount_per_side)

    def map_to_2d(index):
        y = int(index / amount_per_side)

        if y % 2:
            return y, (index % amount_per_side)
        else:
            return y, (amount_per_side - 1 - index % amount_per_side)

    screen.fill((50, 50, 50))

    colors = [c for c in Color.different_colors(hist_count, 100, 40)]
    random.shuffle(colors)

    index = 0
    for i in range(hist_count):
        for j in range(sorted_counts[i][1]):
            y, x = map_to_2d(index)
            pg.draw.rect(screen, colors[i], (x * square_side_length, y * square_side_length, square_side_length, square_side_length))
            index += 1

    # add margins
    px_arr = pg.surfarray.pixels3d(screen)
    for x in range(amount_per_side):
        x_pos = x * square_side_length
        for y in range(amount_per_side - 1):
            # check horizontal
            y_pos = y * square_side_length
            first_pixel = px_arr[x_pos, y_pos]
            second_pixel = px_arr[x_pos, y_pos - 1]

            # if the pixels don't have the same color
            if np.any(first_pixel != second_pixel):
                for i in range(square_side_length):
                    px_arr[x_pos + i, y_pos - 1: y_pos] = [50, 50, 50]

            # check vertical
            second_pixel = px_arr[x_pos - 1, y_pos]
            if np.any(first_pixel != second_pixel):
                for i in range(square_side_length):
                    px_arr[x_pos - 1: x_pos, y_pos + i] = [50, 50, 50]
    del px_arr


def draw(dt):
    pass


keydown_func = {
    pg.K_r: init
}


init()
loop = True
while loop:
    clock.tick(fps_cap)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_func[e.key]()
            except:
                sys.stderr.write("No such Key!")
                sys.stderr.flush()

    # screen.fill(background_color)
    draw(clock.get_time() / 1000)
    # text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    # screen.blit(text, (10, 10))
    pg.display.flip()
pg.quit()
