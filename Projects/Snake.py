import pygame as pg
import sys
import time
import random


# settings
game_size = 10, 10
square_size = 80
background_color = 50, 50, 50
snake_color = 30, 230, 50
goal_color = 240, 30, 30

window_size = game_size[0] * square_size, game_size[1] * square_size


pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Snake!")
clock = pg.time.Clock()
game_over_text = pg.font.SysFont("comicsansms", 200).render("GameOver!", True, (255, 100, 30))


# variables
snake = [[4, 4], [4, 5], [4, 6], [4, 7]]
goal = [7, 7]
direction = [1, 0]
head_pos = 0


directions = {
    "up": [0, -1],
    "down": [0, 1],
    "right": [1, 0],
    "left": [-1, 0],
}


def init():
    global snake, goal, head_pos
    snake = [[4, 4], [4, 5], [4, 6], [4, 7]]
    goal = [7, 7]
    head_pos = len(snake) - 1
    direction = [1, 0]
    random_goal()



def game_over():
    screen.blit(game_over_text, (200, 200))
    pg.display.flip()
    time.sleep(2)
    print("game_over")
    init()


def random_goal():
    global goal
    goal = snake[0]
    while goal in snake:
        goal = [random.randint(0, game_size[0] - 1), random.randint(0, game_size[1] - 1)]


def update():
    global head_pos
    # move snake in direction
    if goal in snake:
        snake.insert(head_pos , goal.copy())
        random_goal()
    else:
        old_pos = snake[head_pos]
        head_pos += 1
        if head_pos == len(snake):
            head_pos = 0
        snake[head_pos] = [old_pos[0] + direction[0], old_pos[1] + direction[1]]

    # check if oob
    if 0 > snake[head_pos][0] or snake[head_pos][0] == game_size[0] or 0 > snake[head_pos][1] or snake[head_pos][1] == game_size[1]:
        game_over()
        return
    if snake[head_pos] in snake[:head_pos] + snake[head_pos + 1:]:
        game_over()
        return





def draw():
    screen.fill(background_color)
    for p in snake:
        pg.draw.rect(screen, snake_color, (p[0] * square_size, p[1] * square_size, square_size, square_size))
    pg.draw.rect(screen, goal_color, (goal[0] * square_size, goal[1] * square_size, square_size, square_size))
    pg.display.flip()


def my_quit():
    global loop
    loop = False


def look_down():
    global direction
    direction = directions["down"]


def look_up():
    global direction
    direction = directions["up"]


def look_right():
    global direction
    direction = directions["right"]


def look_left():
    global direction
    direction = directions["left"]


keydown_func = {
    pg.K_ESCAPE: my_quit,
    pg.K_w: look_up,
    pg.K_s: look_down,
    pg.K_a: look_left,
    pg.K_d: look_right,
    pg.K_r: init,
}


init()
loop = True
while loop:
    clock.tick(5)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_func[e.key]()
            except:
                sys.stderr.write("No such Key!")
                sys.stderr.flush()

    update()
    draw()

pg.quit()
