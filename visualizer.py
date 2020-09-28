import pygame as pg

from emulator import get_ball_position, get_box_x0, set_values, get_ball_velocity

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 250
RED = (255, 0, 0)

run = True
Time = 0
TIME_FACTOR = 3

pg.font.init()
font = pg.font.SysFont("Arial", 16)
text = font.render('GeeksForGeeks', True, (0, 0, 0))


class DrawableCannonBall:
    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity

        ball_raw_pos = get_ball_position(0, WINDOW_HEIGHT)
        ball_pos = convert_to_drawable(ball_raw_pos[0], ball_raw_pos[1])
        self.x = ball_pos[0]
        self.y = ball_pos[1]
        self.radius = int(4 + 0.1 * self.mass)


class DrawableBox:
    def __init__(self, mass, x0):
        self.mass = mass
        self.height = DEFAULT_BOX_HEIGHT
        self.width = DEFAULT_BOX_WIDTH
        self.x = x0 + DEFAULT_BOX_WIDTH // 2
        self.y = 0


CannonBall = None
Box = None
DEFAULT_BOX_HEIGHT = WINDOW_HEIGHT // 6
DEFAULT_BOX_WIDTH = WINDOW_WIDTH // 10


def change_text(new_text):
    global text
    text = font.render(new_text, True, (0, 0, 0))


def handle_keys():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            global run
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False


def convert_to_drawable(x, y):
    x = int(x)
    y = int(WINDOW_HEIGHT - y)
    return [x, y]


def draw_everything(window):
    window.fill([255, 255, 255])
    global CannonBall
    ball_pos = convert_to_drawable(CannonBall.x, CannonBall.y)
    pg.draw.circle(window, RED, (ball_pos[0], ball_pos[1]), CannonBall.radius)
    global Box
    box_pos = convert_to_drawable(Box.x, Box.y)
    pg.draw.rect(window, (0, 255, 255), (box_pos[0], box_pos[1] - Box.height, Box.width, Box.height))
    new_text = 'Х: {0} Y: {1} V: {2}m/s'.format(str(ball_pos[0]), str(WINDOW_HEIGHT - ball_pos[1]), str(CannonBall.velocity))
    change_text(new_text)
    window.blit(text, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))


def emulate_physics():
    global CannonBall
    global Time
    updateTime = round(Time * TIME_FACTOR, 2)
    ball_pos = get_ball_position(updateTime, WINDOW_HEIGHT)
    ball_velocity = abs(round(get_ball_velocity(updateTime), 2))
    CannonBall.x = ball_pos[0]
    CannonBall.y = ball_pos[1]
    CannonBall.velocity = ball_velocity
    if CannonBall.y <= 0:
        Time = 0


def init_values(m1, m2, v1):
    set_values(m1, m2, v1)
    global CannonBall
    CannonBall = DrawableCannonBall(m1, v1)
    global Box
    box_x0 = get_box_x0(WINDOW_HEIGHT - DEFAULT_BOX_HEIGHT)
    Box = DrawableBox(m2, box_x0)


def visualize(m1, m2, v1):
    global run
    run = True
    timer_period = 30
    init_values(m1, m2, v1)
    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("Математическая модель")
    global Time

    while run:
        Time += 1 / timer_period
        handle_keys()
        emulate_physics()
        draw_everything(window)
        pg.display.update()
        pg.time.delay(timer_period)
    pg.quit()
