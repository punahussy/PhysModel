import math
from scipy import constants

ball_mass = 0  # kg
ball_start_velocity = 0  # m/s
box_mass = 0  # kg
ANGLE = 45  # degrees
FRICTION_COEFFICIENT = 0.58  # concrete
GRAVITY_STRENGTH = 9.8
last_case = (1, 5, 15)

BALL_MAX_MASS = 220
BALL_MAX_VELOCITY = constants.speed_of_light


def emulate(m1: float, m2: float, v: float):
    if input_is_valid(m1, m2, v):
        global ball_mass
        ball_mass = m1
        global box_mass
        box_mass = m2
        global ball_start_velocity
        ball_start_velocity = v
        global last_case
        last_case = (m1, m2, v)
        print("Пройденное растояние: {} метров".format(round(calculateDistance(), 2)))
    else:
        print("Введено некорректное значение")


def set_values(m1: float, m2: float, v: float):
    if input_is_valid(m1, m2, v):
        global ball_mass
        ball_mass = m1
        global box_mass
        box_mass = m2
        global ball_start_velocity
        ball_start_velocity = v


def calculateDistance():
    box_velocity = (ball_mass * ball_start_velocity * math.sin(math.radians(ANGLE))) / (ball_mass + box_mass)
    print("Ящик развил скорость: {} м/c".format(round(box_velocity), 2))
    friction = 2 * FRICTION_COEFFICIENT * GRAVITY_STRENGTH
    distance = math.pow(box_velocity, 2) / friction
    return distance


def input_is_valid(m1, m2, v):
    if BALL_MAX_MASS < m1 or m1 <= 0:
        print(" [!]Ошибка: \n [!]Масса ядра должна быть положительной и не превышать {} кг".format(BALL_MAX_MASS))
        return False
    if m2 <= 0:
        print(" [!]Ошибка: \n [!]Масса ящика должна быть положительной")
        return False
    if BALL_MAX_VELOCITY < v or v <= 0:
        print(" [!]Ошибка: \n [!]Скорость должна быть положительной и не превышать {} м/с".format(BALL_MAX_VELOCITY))
        return False
    return True


def get_ball_position(time, height):
    hor_velocity = ball_start_velocity * math.sin(math.radians(ANGLE))
    vert_velocity = ball_start_velocity * math.cos(math.radians(ANGLE))

    gravity_acceleration = (GRAVITY_STRENGTH * math.pow(time, 2)) / 2

    x = (ball_start_velocity + hor_velocity) * time
    y = height - vert_velocity * time - gravity_acceleration
    return [x, y]


def get_ball_velocity(time):
    gravity_deflection = 2 * ball_start_velocity * GRAVITY_STRENGTH * time * math.cos(math.radians(ANGLE))
    gravity_affection = GRAVITY_STRENGTH * GRAVITY_STRENGTH * time * time
    vt = ball_start_velocity - gravity_deflection + gravity_affection
    return vt


def get_box_x0(height):
    hor_velocity = ball_start_velocity * math.sin(math.radians(ANGLE))
    vert_velocity = ball_start_velocity * math.cos(math.radians(ANGLE))
    gravity_affection = math.sqrt((2 * (height - vert_velocity)) / GRAVITY_STRENGTH)
    x0 = hor_velocity * gravity_affection
    return x0


def get_box_pos(time):
    pass
