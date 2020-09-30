import pygame as pg

from emulator import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 250
RED = (255, 0, 0)

Run = True
Time = 0
TIME_FACTOR = 3
Impacted = False

pg.font.init()
Font = pg.font.SysFont("Arial", 16)
Ball_info = Font.render('', True, (0, 0, 0))
Box_info = Font.render('', True, (0, 0, 0))


class DrawableCannonBall:
    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity

        ball_raw_pos = get_ball_position(0)
        ball_pos = convert_to_drawable(ball_raw_pos[0], ball_raw_pos[1])
        self.x = ball_pos[0]
        self.y = ball_pos[1]
        self.radius = int(4 + 0.1 * self.mass)


class DrawableBox:
    def __init__(self, mass, x0):
        self.mass = mass
        self.height = DEFAULT_BOX_HEIGHT
        self.width = DEFAULT_BOX_WIDTH
        self.x = x0
        self.x0 = x0
        self.y = 0
        self.velocity = 0


CannonBall = None
Box = None
DEFAULT_BOX_HEIGHT = WINDOW_HEIGHT // 6
DEFAULT_BOX_WIDTH = WINDOW_WIDTH // 10


def update_displayed_info():
    global Ball_info
    ball_params = convert_to_drawable(CannonBall.x, CannonBall.y)
    new_ball_info = 'Ядро: Х: {0} Y: {1} V: {2}m/s'.format(str(ball_params[0]), str(ball_params[1]),
                                                           str(round(CannonBall.velocity, 2)))
    Ball_info = Font.render(new_ball_info, True, (0, 0, 0))
    global Box_info
    box_params = convert_to_drawable(Box.x, Box.y)
    new_box_info = 'Ящик: Х: {0} Y: {1} V: {2}m/s'.format(str(box_params[0]), str(box_params[1]),
                                                          str(round(Box.velocity, 2)))
    Box_info = Font.render(new_box_info, True, (0, 0, 0))


def reset_box_pos():
    update_time = round(Time * TIME_FACTOR, 2)
    Box.velocity = get_box_current_velocity(update_time)
    Box.x = Box.x0 = get_box_x0()
    CannonBall.x = 0
    CannonBall.y = 0


def handle_keys():
    global Time
    global Impacted
    global Box
    for event in pg.event.get():
        if event.type == pg.QUIT:
            global Run
            Run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                Run = False
            if event.key == pg.K_r:
                Impacted = False
                Time = 0
                reset_box_pos()


def convert_to_drawable(x, y):
    x = int(x)
    y = int(WINDOW_HEIGHT - y)
    return [x, y]


def draw_everything(window):
    window.fill([255, 255, 255])
    global CannonBall
    global Box
    if not Impacted:
        ball_pos = convert_to_drawable(CannonBall.x, CannonBall.y)
        pg.draw.circle(window, RED, (ball_pos[0], ball_pos[1]), CannonBall.radius)
    fix_box_pos = DEFAULT_BOX_HEIGHT // 3 if Box.x0 < (WINDOW_WIDTH // 2) else 0
    box_pos = convert_to_drawable(Box.x + fix_box_pos, Box.y)
    pg.draw.rect(window, (0, 255, 255), (box_pos[0], box_pos[1] - Box.height, Box.width, Box.height))
    window.blit(Ball_info, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    window.blit(Box_info, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 32))


def emulate_physics():
    global Time
    global Impacted
    global CannonBall
    global Box
    update_time = round(Time * TIME_FACTOR, 2)
    if Impacted:
        Box.velocity = get_box_current_velocity(update_time)
        Box.x = get_box_pos(update_time)
    else:
        Box.velocity = 0
        ball_pos = get_ball_position(update_time)
        ball_velocity = abs(round(get_ball_velocity(update_time), 2))
        CannonBall.x = ball_pos[0]
        CannonBall.y = ball_pos[1]
        CannonBall.velocity = ball_velocity
        if Box.x0 < WINDOW_WIDTH // 2:
            if CannonBall.y - DEFAULT_BOX_HEIGHT <= 0:
                Impacted = True
                Time = 0
        else:
            if CannonBall.y - CannonBall.radius < 0:
                Impacted = True
                Time = 0
    update_displayed_info()


def init_values(m1, m2, v1):
    set_values(m1, m2, v1, WINDOW_HEIGHT - DEFAULT_BOX_HEIGHT)
    global CannonBall
    CannonBall = DrawableCannonBall(m1, v1)
    global Box
    box_x0 = get_box_x0()
    Box = DrawableBox(m2, box_x0)


def visualize(m1, m2, v1):
    print("ВНИМАНИЕ: В режиме визуализации численная высота падения \nh в метрах равна высоте окна в пикселях")
    print('Текущая высота окна: {0} пикселей'.format(WINDOW_HEIGHT))
    global Run
    Run = True
    global Time
    Time = 0
    timer_period = 30
    init_values(m1, m2, v1)
    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("Математическая модель")

    while Run:
        Time += 1 / timer_period
        handle_keys()
        emulate_physics()
        draw_everything(window)
        pg.display.update()
        pg.time.delay(timer_period)
    pg.quit()
